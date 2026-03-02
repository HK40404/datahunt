"""LangGraph SQL 生成 Benchmark

对整个 Text-to-SQL 流程进行性能评估，计算 SQL 生成准确率。
"""

import argparse
import asyncio
import json
import logging
import signal
import sys
import time
from datetime import date
from decimal import Decimal
from pathlib import Path

from config.log import PROJECT_LOGGER_NAME
from data_types.message import Message
from graph.graph import text_to_sql
from graph.sql_executor import SQLExecutor
from tracing.tracing import new_trace_id

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

def _save_intermediate_result(
    results: list[dict],
    test_data: list[dict],
    output_dir: Path,
    exec_accuracy: bool
) -> None:
    """保存中间结果（用于程序意外退出时恢复）"""
    try:
        # 计算当前进度
        valid_results = [r for r in results if r.get('error') is None]
        error_count = len(results) - len(valid_results)

        # 添加难度信息
        difficulty_groups: dict[str, list[dict]] = {}
        for result in results:
            difficulty = "unknown"
            for item in test_data:
                if item.get('question_id') == result['question_id']:
                    difficulty = item.get('difficulty', 'unknown')
                    break
            result['difficulty'] = difficulty
            if difficulty not in difficulty_groups:
                difficulty_groups[difficulty] = []
            difficulty_groups[difficulty].append(result)

        # 计算执行准确率
        exec_accuracy_score = None
        exec_difficulty_accuracy = {}
        if exec_accuracy:
            exec_valid_results = [r for r in valid_results if 'exec_match' in r]
            if exec_valid_results:
                exec_correct = sum(1 for r in exec_valid_results if r.get('exec_match', False))
                exec_accuracy_score = exec_correct / len(exec_valid_results)
                for difficulty, group_results in difficulty_groups.items():
                    exec_group = [r for r in group_results if r.get('error') is None and 'exec_match' in r]
                    if exec_group:
                        exec_correct = sum(1 for r in exec_group if r.get('exec_match', False))
                        exec_difficulty_accuracy[difficulty] = exec_correct / len(exec_group)

        # 计算耗时统计
        valid_elapsed_times = [r['elapsed_time'] for r in valid_results]
        latency_stats = calculate_latency_stats(valid_elapsed_times)

        # 构建输出数据
        output_data = {
            'total_questions': len(test_data),
            'completed_questions': len(results),
            'valid_question_count': len(valid_results),
            'error_count': error_count,
            'exec_accuracy_enabled': exec_accuracy,
            'metrics': {
                'execution_accuracy': exec_accuracy_score,
                'execution_difficulty_accuracy': exec_difficulty_accuracy
            },
            'latency': {
                'tp50': latency_stats['tp50'],
                'tp80': latency_stats['tp80'],
                'tp90': latency_stats['tp90'],
                'tp95': latency_stats['tp95'],
                'tp99': latency_stats['tp99'],
                'avg': latency_stats['avg'],
                'total': latency_stats['total'],
                'count': latency_stats['count']
            },
            'results': results
        }

        # 保存到文件
        output_file = output_dir / 'langgraph_eval_result.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2, cls=DecimalEncoder)

        logger.debug(f"   已保存中间结果 ({len(results)}/{len(test_data)} 问题)")
    except Exception as e:
        logger.warning(f"   保存中间结果失败: {e}")


class DecimalEncoder(json.JSONEncoder):
    """自定义 JSON 编码器，处理 Decimal 类型"""

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


def format_time(seconds: float) -> str:
    """将秒数转换为 hh:mm:ss 格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def load_test_data(question_file: Path) -> list[dict]:
    """从测试数据文件加载问题列表"""
    with open(question_file, encoding='utf-8') as f:
        return json.load(f)


def load_question_ids(file_path: Path) -> list[int]:
    """
    从文件加载问题ID列表

    支持格式:
    - JSON数组: [1471, 1472, 1473]
    - 每行一个ID:
      1471
      1472
      1473
    """
    with open(file_path, encoding='utf-8') as f:
        content = f.read().strip()

        # 尝试JSON数组格式
        if content.startswith('['):
            return json.loads(content)

        # 每行一个ID格式
        ids = []
        for line in content.split('\n'):
            line = line.strip()
            if line and line.isdigit():
                ids.append(int(line))
        return ids


def filter_by_ids(test_data: list[dict], question_ids: list[int]) -> list[dict]:
    """根据问题ID列表过滤测试数据"""
    if not question_ids:
        return test_data

    filtered = [item for item in test_data if item.get('question_id') in question_ids]
    missing_ids = set(question_ids) - {item.get('question_id') for item in filtered}

    if missing_ids:
        logger.warning(f"   警告: 以下问题ID未找到: {sorted(missing_ids)}")

    return filtered


def calculate_percentile(values: list[float], percentile: float) -> float:
    """计算百分位数"""
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = int(len(sorted_values) * percentile / 100)
    return sorted_values[min(index, len(sorted_values) - 1)]


def calculate_latency_stats(elapsed_times: list[float]) -> dict:
    """计算耗时统计信息"""
    if not elapsed_times:
        return {
            'tp50': 0.0, 'tp80': 0.0, 'tp90': 0.0,
            'tp95': 0.0, 'tp99': 0.0, 'avg': 0.0,
            'total': 0.0, 'count': 0
        }

    return {
        'tp50': calculate_percentile(elapsed_times, 50),
        'tp80': calculate_percentile(elapsed_times, 80),
        'tp90': calculate_percentile(elapsed_times, 90),
        'tp95': calculate_percentile(elapsed_times, 95),
        'tp99': calculate_percentile(elapsed_times, 99),
        'avg': sum(elapsed_times) / len(elapsed_times),
        'total': sum(elapsed_times),
        'count': len(elapsed_times)
    }


async def run_single_question(
    question: str,
    evidence: str,
    database: str
) -> dict:
    """
    运行单个问题的 LangGraph 流程

    Args:
        question: 用户问题
        evidence: 证据/外部知识
        database: 数据库名称

    Returns:
        包含生成结果和耗时的字典
    """
    # 创建 trace_id
    trace_id = new_trace_id()
    start_time = time.time()

    try:
        # 调用 text_to_sql 函数
        result = await text_to_sql({
            "question": "",
            "messages": [Message.user_message(question)],
            "evidence": evidence,
            "database": database,
            "generated_sql": "",
            "matched_tables": [],
            "DDL": [],
            "exec_result": [],
            "exec_error": "",
            "validate_error": None,
            "review_result": True,
            "review_comment": "",
            "fix_count": 0
        })

        elapsed_time = time.time() - start_time

        return {
            'trace_id': trace_id,
            'generated_sql': result.get('generated_sql', ''),
            'exec_error': result.get('exec_error', ''),
            'exec_result': result.get('exec_result', []),
            'review_result': result.get('review_result'),
            'review_comment': result.get('review_comment', ''),
            'elapsed_time': elapsed_time,
            'error': None
        }
    except Exception as e:
        logger.error(f"   运行问题失败: {e}")
        elapsed_time = time.time() - start_time
        return {
            'trace_id': trace_id,
            'generated_sql': '',
            'exec_error': str(e),
            'exec_result': [],
            'review_result': None,
            'review_comment': '',
            'elapsed_time': elapsed_time,
            'error': str(e)
        }


def _signal_handler(signum, frame, results_ref, test_data_ref, output_dir_ref):
    """信号处理：保存结果后退出"""
    results = results_ref
    test_data = test_data_ref
    output_dir = output_dir_ref

    logger.info(f"\n⚠️  检测到信号 {signum}，正在保存当前进度...")
    if results and test_data:
        # 确保输出目录存在
        output_dir.mkdir(parents=True, exist_ok=True)
        _save_intermediate_result(results, test_data, output_dir, True)

        # 计算并打印当前准确率
        valid_results = [r for r in results if r.get('error') is None]
        exec_valid = [r for r in valid_results if 'exec_match' in r]
        if exec_valid:
            exec_correct = sum(1 for r in exec_valid if r.get('exec_match', False))
            exec_acc = exec_correct / len(exec_valid)

            # 计算按难度统计
            difficulty_groups: dict[str, list[dict]] = {}
            for result in results:
                difficulty = "unknown"
                for item in test_data:
                    if item.get('question_id') == result.get('question_id'):
                        difficulty = item.get('difficulty', 'unknown')
                        break
                if difficulty not in difficulty_groups:
                    difficulty_groups[difficulty] = []
                difficulty_groups[difficulty].append(result)

            # 输出最终统计结果
            logger.info("\n" + "=" * 60)
            logger.info("📊 中止时最终评估结果")
            logger.info("=" * 60)
            logger.info(f"   总问题数: {len(test_data)}")
            logger.info(f"   完成问题: {len(results)}")
            logger.info(f"   投票通过: {exec_correct} ({exec_acc * 100:.1f}%)")
            logger.info(f"   未通过: {len(exec_valid) - exec_correct} ({(1 - exec_acc) * 100:.1f}%)")

            logger.info("\n📊 按难度统计（已完成）:")
            for diff in ['simple', 'moderate', 'challenging', 'unknown']:
                if diff in difficulty_groups:
                    diff_results = difficulty_groups[diff]
                    diff_valid = [r for r in diff_results if r.get('error') is None and 'exec_match' in r]
                    if diff_valid:
                        diff_correct = sum(1 for r in diff_valid if r.get('exec_match', False))
                        diff_acc = diff_correct / len(diff_valid)
                        logger.info(f"   {diff}: {diff_correct}/{len(diff_valid)} ({diff_acc * 100:.1f}%)")

            # 统计生成SQL失败和执行失败的问题
            sql_generation_failed = [r.get('question_id') for r in results if not r.get('generated_sql')]
            sql_execution_failed = [r.get('question_id') for r in results if r.get('exec_error')]

            if sql_generation_failed:
                logger.info(f"\n⚠️  生成SQL失败: {len(sql_generation_failed)} 个")
            if sql_execution_failed:
                logger.info(f"⚠️  执行SQL失败: {len(sql_execution_failed)} 个")

        logger.info(f"\n   结果已保存到: {output_dir / 'langgraph_eval_result.json'}")
    else:
        logger.info("   无结果可保存")

    sys.exit(0)




async def evaluate_langgraph(
    question_file: Path,
    output_dir: Path,
    concurrency: int = 1,
    limit: int | None = None,
    question_ids: list[int] = [],
    database: str = "bird",
    exec_accuracy: bool = False,
    dry_run: bool = False,
    epochs: int = 1,
    tolerance: float = 0.001
) -> None:
    """
    对 LangGraph SQL 生成进行评估

    Args:
        question_file: 测试数据文件路径
        output_dir: 输出目录
        concurrency: 并发度，默认1（串行执行）
        limit: 限制测试样本数量，默认None（全部）
        question_ids: 指定测试的问题ID列表，默认None（全部）
        database: 数据库名称
        exec_accuracy: 是否计算执行准确率，默认False
        dry_run: 干跑模式，只打印问题进度不执行评估
        epochs: 评估轮数，默认1轮。每个问题最多评估epochs次，有一次通过就算成功
        tolerance: 数值比较误差容忍度，默认0.001
    """
    logger.info("📊 开始 LangGraph SQL 生成评估...")
    logger.info(f"   数据库: {database}")
    logger.info(f"   并发度: {concurrency}")
    logger.info(f"   评估轮数: {epochs}")
    logger.info(f"   干跑模式: {'开启' if dry_run else '关闭'}")
    logger.info(f"   样本限制: {limit if limit else '全部'}")
    if question_ids:
        logger.info(f"   指定问题ID: {question_ids}")
    logger.info(f"   执行准确率: {'开启' if exec_accuracy else '关闭'}")
    logger.info(f"   误差容忍度: {tolerance}")

    # 初始化 SQL 执行器（用于执行准确率评估）
    sql_executor = SQLExecutor(tolerance=tolerance)

    # 加载测试数据
    logger.info("   加载测试数据...")
    test_data = load_test_data(question_file)
    logger.info(f"   已加载 {len(test_data)} 个测试问题")

    # 按问题ID过滤
    if question_ids:
        test_data = filter_by_ids(test_data, question_ids)
        logger.info(f"   按ID过滤后: {len(test_data)} 个问题")

    # 限制样本数量
    if limit and limit > 0:
        test_data = test_data[:limit]
        logger.info(f"   限制为前 {limit} 个问题")

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 初始化结果列表（用于信号处理）
    results: list[dict] = []

    # 设置信号处理器（传递引用）
    def signal_handler(signum, frame):
        _signal_handler(signum, frame, results, test_data, output_dir)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # 干跑模式：只打印问题进度
    if dry_run:
        logger.info("   干跑模式：只打印问题列表")
        for idx, item in enumerate(test_data, 1):
            question_id = item.get('question_id')
            query_text = item.get('question', '')
            difficulty = item.get('difficulty', 'unknown')
            progress = (idx / len(test_data)) * 100
            logger.info(
                f"[{progress:5.1f}%] ID:{question_id} | 难度:{difficulty} | 问题: {query_text}"
            )
        logger.info(f"   共 {len(test_data)} 个问题")
        logger.info("   干跑完成，未执行实际评估")
        return

    # 执行评估

    # 初始化时间跟踪变量
    first_question_start_time = None
    last_question_end_time = None

    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(concurrency)

    async def process_single_epoch(epoch: int, all_items: list[dict], results_list: list[dict]):
        """处理单个轮次，返回所有问题的执行结果"""
        # 初始化时间跟踪变量
        nonlocal first_question_start_time
        if first_question_start_time is None:
            first_question_start_time = time.time()

        # 进度跟踪
        progress_state = {'completed': 0, 'correct': 0, 'total': len(all_items), 'start_time': time.time()}
        progress_lock = asyncio.Lock()

        async def process_item(item: dict):
            async with semaphore:
                query_text = item.get('question', '')
                evidence = item.get('evidence', '')
                ground_truth_sql = item.get('SQL', '')
                db_id = item.get('db_id', '')
                question_id = item.get('question_id')
                difficulty = item.get('difficulty', 'unknown')

                result = await run_single_question(query_text, evidence, database)

                # 执行准确率评估
                exec_match = None
                generated_result = result.get('exec_result', [])
                ground_truth_result = []
                generated_success = len(result.get('exec_error', '')) == 0
                gt_success = True
                gt_error = None
                if exec_accuracy and sql_executor and result['error'] is None:
                    # 使用 graph 执行的结果
                    generated_result = result.get('exec_result', [])
                    generated_success = len(result.get('exec_error', '')) == 0

                    # 执行预期 SQL
                    gt_success, ground_truth_result, gt_error = sql_executor.execute_query(
                        db_id, ground_truth_sql
                    )

                    # 对比结果
                    exec_match = sql_executor._compare_results(generated_result, ground_truth_result)

                # 打印完整SQL
                logger.info(f"       生成SQL:\n       {result['generated_sql']}")
                if ground_truth_sql:
                    logger.info(f"       预期SQL:\n       {ground_truth_sql}")
                # 打印结果对比
                if exec_accuracy and result['error'] is None:
                    logger.info(f"       生成结果 ({len(generated_result)}行): {generated_result}")
                    logger.info(f"       预期结果 ({len(ground_truth_result)}行): {ground_truth_result}")

                match_status = "✓" if exec_match else "✗" if exec_match is not None else "-"

                # 更新进度计数
                async with progress_lock:
                    progress_state['completed'] += 1
                    if exec_match:
                        progress_state['correct'] += 1
                    completed = progress_state['completed']
                    correct = progress_state['correct']
                    total = progress_state['total']
                    progress_pct = (completed / total) * 100
                    accuracy = (correct / completed * 100) if completed > 0 else 0.0

                    # 计算 ETA 剩余时间
                    elapsed = time.time() - progress_state['start_time']
                    if completed > 0:
                        eta_seconds = elapsed * (total - completed) / completed
                    else:
                        eta_seconds = 0

                    # 格式化为 hh:mm:ss
                    eta_formatted = format_time(eta_seconds) if eta_seconds > 0 else "00:00:00"

                    bar_length = 30
                    filled_length = int(bar_length * completed // total)
                    bar = '█' * filled_length + '░' * (bar_length - filled_length)
                    logger.info(
                        f"[{bar}] {progress_pct:5.1f}% | "
                        f"[{completed:3d}/{total}] ID:{question_id} [{difficulty:8}] | "
                        f"{match_status} | Acc:{accuracy:5.1f}% | ETA:{eta_formatted}"
                    )

                # 构建完整结果
                result_data = {
                    'question_id': question_id,
                    'db_id': db_id,
                    'question': item.get('question'),
                    'ground_truth_sql': ground_truth_sql,
                    'generated_sql': result['generated_sql'],
                    'exec_error': result.get('exec_error', ''),
                    'elapsed_time': result['elapsed_time'],
                    'error': result['error'],
                    'exec_match': exec_match,
                    'generated_result': generated_result,
                    'ground_truth_result': ground_truth_result,
                    'generated_success': generated_success if exec_accuracy else False,
                    'ground_truth_success': gt_success if exec_accuracy else False,
                    'gen_error': result.get('exec_error', '') if not generated_success else None,
                    'gt_error': gt_error if exec_accuracy else None,
                    'difficulty': difficulty,
                    'epoch': epoch
                }

                # 立即同步到 results 列表（用于信号处理）
                results_list.append(result_data)

                return result_data

        tasks = [process_item(item) for item in all_items]
        epoch_results = await asyncio.gather(*tasks)

        return epoch_results

    # 多轮评估
    logger.info(f"   开始多轮评估 (共{epochs}轮)...")

    # 记录每个问题在所有轮次的结果
    all_epoch_results: dict[int, list[dict]] = {}  # question_id -> [result1, result2, ...]

    # 投票函数
    def vote_result(question_id: int, results: list[dict], sql_executor: SQLExecutor) -> tuple:
        """
        对结果进行投票
        返回: (voted_result, is_consensus, has_correct_in_different)
        """
        if not results:
            return None, False, False

        # 按 generated_result 分组（使用 _compare_results 判断是否相同）
        groups = {}  # result_key -> [results...]
        for r in results:
            result_val = r.get('generated_result', [])
            found_group = False
            for key in groups:
                if sql_executor._compare_results(result_val, key):
                    groups[key].append(r)
                    found_group = True
                    break
            if not found_group:
                groups[tuple(sorted([str(k) + str(v) for k, v in (result_val or [{}])[0].items()])) if result_val else tuple()] = [r]

        # 找出最多票的结果
        max_group_key = max(groups.keys(), key=lambda k: len(groups[k]))
        max_voted = groups[max_group_key]
        voted_result = max_voted[0].get('generated_result', [])

        # 检查是否全票通过
        is_consensus = len(max_voted) == len(results)

        # 检查特殊情况：3个不同结果但有正确答案
        has_correct_in_different = False
        if len(groups) == len(results):  # 全部结果都不同
            for r in results:
                if r.get('exec_match', False):
                    has_correct_in_different = True
                    break

        return voted_result, is_consensus, has_correct_in_different

    for epoch in range(1, epochs + 1):
        logger.info(f"\n=== Epoch {epoch}/{epochs} (评估: {len(test_data)}题) ===")

        # 执行本轮评估（所有问题）
        epoch_results = await process_single_epoch(epoch, test_data, results)

        # 记录结果
        for r in epoch_results:
            qid = r['question_id']
            if qid not in all_epoch_results:
                all_epoch_results[qid] = []
            all_epoch_results[qid].append(r)

        # 计算本轮通过数
        epoch_passed = sum(1 for r in epoch_results if r.get('exec_match', False))
        pass_rate = epoch_passed / len(test_data) * 100
        logger.info(f"   Epoch {epoch} 通过: {epoch_passed}题 ({pass_rate:.1f}%)")

    last_question_end_time = time.time()

    # 计算累计时间（第一个问题开始到最后一个问题结束）
    cumulative_time = 0
    if first_question_start_time and last_question_end_time:
        cumulative_time = last_question_end_time - first_question_start_time
    elif first_question_start_time:
        cumulative_time = time.time() - first_question_start_time

    logger.info("\n✅ LangGraph SQL 生成评估完成！")

    # 计算各轮通过率
    total_questions = len(test_data)
    pass_rates_by_epoch = {}  # epoch -> pass_rate

    # 统计每轮的通过数
    for epoch in range(1, epochs + 1):
        epoch_passed = sum(1 for results in all_epoch_results.values()
                          for r in results if r.get('epoch') == epoch and r.get('exec_match', False))
        pass_rate = epoch_passed / total_questions * 100
        pass_rates_by_epoch[epoch] = pass_rate

    # 投票统计
    voted_passed = 0
    special_cases = []  # 多轮结果不同但包含正确答案的问题

    # 按难度统计投票通过情况
    voted_passed_by_difficulty = {'simple': 0, 'moderate': 0, 'challenging': 0, 'unknown': 0}

    # 获取 ground_truth_result 映射
    gt_result_map = {}  # question_id -> ground_truth_result
    for qid, results in all_epoch_results.items():
        if results:
            gt_result_map[qid] = results[0].get('ground_truth_result', [])

    # 构建按 epoch 组织的结果（1, 2, ...）
    epoch_organized_results = {}
    for epoch in range(1, epochs + 1):
        epoch_organized_results[epoch] = []
        for qid, results in all_epoch_results.items():
            # 找到该 epoch 的结果
            for r in results:
                if r.get('epoch') == epoch:
                    # 获取难度
                    difficulty = 'unknown'
                    for item in test_data:
                        if item.get('question_id') == qid:
                            difficulty = item.get('difficulty', 'unknown')
                            break
                    # 添加 difficulty 字段
                    r['difficulty'] = difficulty
                    epoch_organized_results[epoch].append(r)
                    break

    # 投票统计
    voted_passed = 0
    special_cases = []  # 多轮结果不同但包含正确答案的问题

    # 按难度统计投票通过情况
    voted_passed_by_difficulty = {'simple': 0, 'moderate': 0, 'challenging': 0, 'unknown': 0}

    # 获取 ground_truth_result 映射
    gt_result_map = {}  # question_id -> ground_truth_result
    for qid, results in all_epoch_results.items():
        if results:
            gt_result_map[qid] = results[0].get('ground_truth_result', [])

    for qid, results in all_epoch_results.items():
        if not results:
            continue

        # 获取预期结果
        gt_result = gt_result_map.get(qid, [])

        # 投票
        voted_result, is_consensus, has_correct_in_different = vote_result(qid, results, sql_executor)

        # 检查投票结果是否与预期匹配
        # 注意：当 exec_match 为 None 时（生成失败），不应算作通过
        voted_match = sql_executor._compare_results(voted_result, gt_result)
        has_true_exec_match = any(r.get('exec_match') for r in results)
        if voted_match and has_true_exec_match:
            voted_passed += 1
            # 记录难度
            for item in test_data:
                if item.get('question_id') == qid:
                    d = item.get('difficulty', 'unknown')
                    voted_passed_by_difficulty[d] = voted_passed_by_difficulty.get(d, 0) + 1
                    break

        # 记录特殊情况
        if has_correct_in_different:
            special_cases.append({
                'question_id': qid,
                'question': results[0].get('question', ''),
                'all_results': results
            })

    final_pass_rate = voted_passed / total_questions * 100

    # 计算累计通过率（至少有一轮通过）
    at_least_one_pass = sum(1 for results in all_epoch_results.values()
                            if any(r.get('exec_match', False) for r in results))
    cumulative_pass_rate = at_least_one_pass / total_questions * 100

    # 打印最终统计结果
    logger.info("\n" + "="*60)
    logger.info("📊 最终评估结果")
    logger.info("="*60)
    logger.info(f"   总问题数: {total_questions}")
    logger.info(f"   投票通过: {voted_passed} ({final_pass_rate:.1f}%)")
    logger.info(f"   累计通过（至少一轮）: {at_least_one_pass} ({cumulative_pass_rate:.1f}%)")
    logger.info(f"   未通过: {total_questions - at_least_one_pass} ({100-cumulative_pass_rate:.1f}%)")
    logger.info(f"   累计耗时: {cumulative_time:.2f}秒")

    # 打印各轮通过率
    logger.info("\n📈 各轮通过率:")
    for epoch in range(1, epochs + 1):
        logger.info(f"   通过率@{epoch}: {pass_rates_by_epoch[epoch]:.1f}%")

    # 打印特殊情况（只有多轮评估时才有意义）
    if special_cases and epochs > 1:
        logger.info("\n⚠️  多轮结果不一致但包含正确答案的问题:")
        for case in special_cases:
            logger.info(f"   ID:{case['question_id']} - {case['question']}")

    # 按难度统计
    logger.info("\n📊 按难度统计（投票结果）:")
    for diff in ['simple', 'moderate', 'challenging', 'unknown']:
        diff_total = sum(1 for item in test_data if item.get('difficulty') == diff)
        diff_passed = voted_passed_by_difficulty.get(diff, 0)
        if diff_total > 0:
            diff_rate = diff_passed / diff_total * 100
            logger.info(f"   {diff}: {diff_passed}/{diff_total} ({diff_rate:.1f}%)")

    # 统计生成SQL失败和执行失败的问题
    sql_generation_failed = []  # generated_sql 为空
    sql_execution_failed = []   # exec_error 不为空

    for qid, results in all_epoch_results.items():
        # 获取第一轮的结果（用于检查生成和执行状态）
        first_result = results[0] if results else {}
        generated_sql = first_result.get('generated_sql', '')
        exec_error = first_result.get('exec_error', '')

        if not generated_sql:
            sql_generation_failed.append(qid)
        if exec_error:
            sql_execution_failed.append(qid)

    logger.info("\n⚠️  生成SQL失败的问题:")
    if sql_generation_failed:
        logger.info(f"   共 {len(sql_generation_failed)} 个: {sql_generation_failed}")
    else:
        logger.info("   无")

    logger.info("\n⚠️  执行SQL失败的问题:")
    if sql_execution_failed:
        logger.info(f"   共 {len(sql_execution_failed)} 个: {sql_execution_failed}")
    else:
        logger.info("   无")

    # 保存结果
    output_data = {
        'total_questions': total_questions,
        'epochs': epochs,
        'voted_passed_count': voted_passed,
        'voted_pass_rate': final_pass_rate,
        'cumulative_pass_count': at_least_one_pass,
        'cumulative_pass_rate': cumulative_pass_rate,
        'pass_rates_by_epoch': pass_rates_by_epoch,
        'voted_passed_by_difficulty': voted_passed_by_difficulty,
        'special_cases_count': len(special_cases),
        'special_cases': [{'question_id': c['question_id'], 'question': c['question']} for c in special_cases],
        'sql_generation_failed_count': len(sql_generation_failed),
        'sql_generation_failed_ids': sql_generation_failed,
        'sql_execution_failed_count': len(sql_execution_failed),
        'sql_execution_failed_ids': sql_execution_failed,
        'all_epoch_results': epoch_organized_results,  # 按 epoch 轮次组织（epoch_1, epoch_2, ...）
        'database': database,
        'concurrency': concurrency,
        'limit': limit,
        'exec_accuracy_enabled': exec_accuracy,
        'cumulative_time': cumulative_time,
    }

    output_file = output_dir / 'langgraph_eval_result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2, cls=DecimalEncoder)

    logger.info(f"\n   结果已保存到: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='LangGraph SQL 生成 Benchmark')
    parser.add_argument(
        '--questions',
        type=str,
        default='src/pipeline/data/mini_dev_mysql.json',
        help='测试数据文件路径'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='src/pipeline/output/langgraph',
        help='输出目录'
    )
    parser.add_argument(
        '--concurrency',
        type=int,
        default=20,
        help='并发度，默认20。'
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='限制测试样本数量，默认None（全部）。例如 --limit 20 表示只测试前20条'
    )
    parser.add_argument(
        '--database',
        type=str,
        default='bird',
        help='数据库名称，默认bird'
    )
    parser.add_argument(
        '--exec-accuracy',
        action='store_true',
        help='是否计算执行准确率（在数据库上执行 SQL 并对比结果）'
    )
    parser.add_argument(
        '--ids-file',
        type=str,
        nargs='?',    # 表示这个参数是可选的（0个或1个）
        const='src/pipeline/data/benchmark/questions.txt', # 只有传了 --ids-file 但没给值时，用这个
        default=None, # 根本没写 --ids-file 时，用这个
        help='指定问题ID文件路径'
    )
    parser.add_argument(
        '--ids',
        type=str,
        default=None,
        help='直接指定问题ID列表，逗号分隔，例如: 1471,1472,1473'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='干跑模式：只打印问题进度，不执行实际评估'
    )
    parser.add_argument(
        '--epochs',
        type=int,
        default=1,
        help='评估轮数，默认1轮。每个问题最多评估epochs次，有一次通过就算成功'
    )
    parser.add_argument(
        '--tolerance',
        type=float,
        default=0.001,
        help='数值比较误差容忍度，默认0.001。例如 --tolerance 0.0001 表示更严格的比较'
    )

    args = parser.parse_args()

    # 加载问题ID
    question_ids = None
    if args.ids_file:
        question_ids = load_question_ids(Path(args.ids_file))
    elif args.ids:
        question_ids = [int(x.strip()) for x in args.ids.split(',') if x.strip().isdigit()]

    asyncio.run(evaluate_langgraph(
        question_file=Path(args.questions),
        output_dir=Path(args.output),
        concurrency=args.concurrency,
        limit=args.limit,
        question_ids=question_ids,
        database=args.database,
        exec_accuracy=args.exec_accuracy,
        dry_run=args.dry_run,
        epochs=args.epochs,
        tolerance=args.tolerance
    ))


if __name__ == '__main__':
    main()
