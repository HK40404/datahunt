"""对检索结果进行rerank并计算评估指标"""

import argparse
import asyncio
import json
import logging
import time
from pathlib import Path

from config import PROJECT_LOGGER_NAME
from graph.reranker import rerank_schemas
from graph.reranker_llm import LLMReranker
from llm.openai import openai_client

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


def format_time(seconds: float) -> str:
    """
    将秒数转换为 hh:mm:ss 格式

    Args:
        seconds: 秒数

    Returns:
        hh:mm:ss 格式的时间字符串
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def load_schema_dict(schema_file: Path) -> dict[str, str]:
    """
    从schema文件中加载表名到schema文本的映射

    Args:
        schema_file: schema文件路径

    Returns:
        表名（小写）到schema文本的字典
    """
    schema_dict = {}

    with open(schema_file, encoding='utf-8') as f:
        content = f.read()

    # 按"Table:"分割
    tables = content.split('\nTable:')

    for i, table_section in enumerate(tables):
        if i == 0:
            # 第一个部分，可能没有"Table:"前缀
            if not table_section.strip().startswith('Table:'):
                continue
            table_section = table_section.strip()
        else:
            # 其他部分，添加回"Table:"前缀
            table_section = 'Table:' + table_section.strip()

        lines = table_section.split('\n')
        if not lines:
            continue

        # 第一行是"Table: xxx"
        first_line = lines[0].strip()
        if not first_line.startswith('Table:'):
            continue

        # 提取表名
        table_name = first_line.replace('Table:', '').strip().lower()

        # 整个section作为schema文本
        schema_text = table_section

        schema_dict[table_name] = schema_text

    return schema_dict


def load_question_map(question_file: Path) -> dict[int, dict]:
    """
    从问题文件中加载question_id到问题信息的映射

    Args:
        question_file: 问题文件路径

    Returns:
        question_id到问题信息的字典
    """
    with open(question_file, encoding='utf-8') as f:
        questions = json.load(f)

    return {q['question_id']: q for q in questions}


def load_question_ids(question_ids_file: Path) -> set[int]:
    """
    从文件中加载问题ID列表

    Args:
        question_ids_file: 问题ID列表文件路径（JSON格式，包含整数列表）

    Returns:
        问题ID集合
    """
    if not question_ids_file.exists():
        return set()

    with open(question_ids_file, encoding='utf-8') as f:
        question_ids = json.load(f)

    return set(question_ids)


def calculate_map(retrieved_tables: list[str], ground_truth_tables: set[str]) -> float:
    """
    计算Mean Average Precision (MAP)

    Args:
        retrieved_tables: 检索到的表列表（已排序）
        ground_truth_tables: 真实相关的表集合

    Returns:
        Average Precision值
    """
    if not ground_truth_tables:
        return 0.0

    relevant_count = 0
    precision_sum = 0.0
    seen_relevant = set()  # 记录已见过的相关表，每个相关表只计算第一次出现

    for i, table in enumerate(retrieved_tables, 1):
        table_lower = table.lower()
        if table_lower in ground_truth_tables and table_lower not in seen_relevant:
            # 只计算每个相关表的第一次出现
            seen_relevant.add(table_lower)
            relevant_count += 1
            precision_at_i = relevant_count / i
            precision_sum += precision_at_i

    if relevant_count == 0:
        return 0.0

    return precision_sum / len(ground_truth_tables)


def calculate_recall_at_k(retrieved_tables: list[str], ground_truth_tables: set[str], k: int) -> float:
    """
    计算Recall@K

    Args:
        retrieved_tables: 检索到的表列表（已排序）
        ground_truth_tables: 真实相关的表集合
        k: K值

    Returns:
        Recall@K值
    """
    if not ground_truth_tables:
        return 0.0

    top_k_tables = set(t.lower() for t in retrieved_tables[:k])
    relevant_in_top_k = len(top_k_tables & ground_truth_tables)

    return relevant_in_top_k / len(ground_truth_tables)


def calculate_precision_at_k(retrieved_tables: list[str], ground_truth_tables: set[str], k: int) -> float:
    """
    计算Precision@K

    Args:
        retrieved_tables: 检索到的表列表（已排序）
        ground_truth_tables: 真实相关的表集合
        k: K值

    Returns:
        Precision@K值
    """
    if k == 0:
        return 0.0

    top_k_tables = set(t.lower() for t in retrieved_tables[:k])
    relevant_in_top_k = len(top_k_tables & ground_truth_tables)

    return relevant_in_top_k / k


def calculate_f1_at_k(retrieved_tables: list[str], ground_truth_tables: set[str], k: int) -> float:
    """
    计算F1@K

    Args:
        retrieved_tables: 检索到的表列表（已排序）
        ground_truth_tables: 真实相关的表集合
        k: K值

    Returns:
        F1@K值
    """
    precision = calculate_precision_at_k(retrieved_tables, ground_truth_tables, k)
    recall = calculate_recall_at_k(retrieved_tables, ground_truth_tables, k)

    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def calculate_percentile(values: list[float], percentile: float) -> float:
    """
    计算百分位数

    Args:
        values: 数值列表
        percentile: 百分位数（0-100），如50表示TP50

    Returns:
        百分位数值
    """
    if not values:
        return 0.0

    sorted_values = sorted(values)
    index = int(len(sorted_values) * percentile / 100)
    return sorted_values[min(index, len(sorted_values) - 1)]


def calculate_latency_stats(elapsed_times: list[float]) -> dict:
    """
    计算耗时统计信息

    Args:
        elapsed_times: 耗时列表（秒）

    Returns:
        包含TP50、TP80、TP85、TP90、TP95、TP99和平均耗时的字典
    """
    if not elapsed_times:
        return {
            'tp50': 0.0,
            'tp80': 0.0,
            'tp85': 0.0,
            'tp90': 0.0,
            'tp95': 0.0,
            'tp99': 0.0,
            'avg': 0.0,
            'total': 0.0,
            'count': 0
        }

    return {
        'tp50': calculate_percentile(elapsed_times, 50),
        'tp80': calculate_percentile(elapsed_times, 80),
        'tp85': calculate_percentile(elapsed_times, 85),
        'tp90': calculate_percentile(elapsed_times, 90),
        'tp95': calculate_percentile(elapsed_times, 95),
        'tp99': calculate_percentile(elapsed_times, 99),
        'avg': sum(elapsed_times) / len(elapsed_times),
        'total': sum(elapsed_times),
        'count': len(elapsed_times)
    }


def calculate_tables_for_recall_one(retrieved_tables: list[str], ground_truth_tables: set[str]) -> int:
    """
    计算达到召回率为1.0时需要的表数

    Args:
        retrieved_tables: 检索到的表列表（已排序）
        ground_truth_tables: 真实相关的表集合

    Returns:
        达到recall=1.0时需要的表数，如果无法达到则返回-1
    """
    if not ground_truth_tables:
        return 0

    # 确保ground_truth_tables中的元素都是小写
    ground_truth_lower = {t.lower() if isinstance(t, str) else str(t).lower() for t in ground_truth_tables}

    found_tables = set()
    for i, table in enumerate(retrieved_tables, 1):
        table_lower = table.lower() if isinstance(table, str) else str(table).lower()
        if table_lower in ground_truth_lower:
            found_tables.add(table_lower)
            if len(found_tables) == len(ground_truth_lower):
                return i

    # 如果无法找到所有ground truth表，返回-1
    return -1


async def evaluate_rerank(
    eval_results_file: Path,
    schema_file: Path,
    question_file: Path,
    output_dir: Path,
    k_list: list[int] = [1, 3, 5, 10],
    reranker_type: str = "reranker",
    batch_size: int = 8,
    question_ids_file: Path = None
) -> None:
    """
    对检索结果进行rerank并计算评估指标

    Args:
        eval_results_file: 评估结果文件路径
        schema_file: schema文件路径
        question_file: 问题文件路径
        output_dir: 输出目录
        k_list: K值列表
        reranker_type: reranker类型，'reranker' 或 'reranker_llm'
        batch_size: 批次大小，用于控制内存使用，默认8
        question_ids_file: 问题ID列表文件路径，如果指定则只评估列表中的问题
    """
    logger.info("📊 开始rerank评估...")
    logger.info(f"   使用reranker类型: {reranker_type}")

    # 初始化reranker
    if reranker_type == "reranker_llm":
        llm_reranker = LLMReranker(client=openai_client)
    elif reranker_type == "reranker":
        llm_reranker = None
    else:
        raise ValueError(f"不支持的reranker类型: {reranker_type}，支持的类型: 'reranker', 'reranker_llm'")

    # 加载数据
    logger.info("   加载数据文件...")
    with open(eval_results_file, encoding='utf-8') as f:
        eval_data = json.load(f)

    schema_dict = load_schema_dict(schema_file)
    question_map = load_question_map(question_file)

    # 加载问题ID列表（如果指定）
    target_question_ids = None
    if question_ids_file:
        loaded_ids = load_question_ids(question_ids_file)
        if loaded_ids:
            target_question_ids = loaded_ids
            logger.info(f"   已加载 {len(target_question_ids)} 个指定问题ID，将只评估这些问题")
        else:
            logger.info("   ⚠️  问题ID文件为空或不存在，将评估所有问题")
            target_question_ids = None  # 确保为空集合时设置为None

    logger.info(f"   已加载 {len(schema_dict)} 个表的schema")
    logger.info(f"   已加载 {len(question_map)} 个问题")

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 第一阶段：收集所有需要rerank的问题数据
    question_data_list = []  # 存储需要rerank的问题数据
    skipped_questions = []  # 存储被跳过的问题

    total_questions = len(eval_data.get('question_results', []))

    for idx, item in enumerate(eval_data.get('question_results', []), 1):
        question_id = item.get('question_id')

        # 如果指定了问题ID列表，只处理列表中的问题
        if target_question_ids is not None and question_id not in target_question_ids:
            continue

        ground_truth_tables = set(t.lower() for t in item.get('ground_truth_tables', []))
        retrieved_tables_augmented = item.get('retrieved_tables_augmented', [])

        # 跳过没有ground truth表的问题
        if not ground_truth_tables:
            skipped_questions.append({
                'question_id': question_id,
                'reason': '无ground truth表',
                'idx': idx
            })
            continue

        # 获取问题文本
        question_info = question_map.get(question_id, {})
        question = question_info.get('question', '')
        evidence = question_info.get('evidence', '')

        # 构建查询文本（使用question + evidence）
        query_text = question
        if evidence:
            query_text = f"{question} {evidence}"

        # 获取表的schema，构建为字典格式
        table_schemas_dict = {}
        table_names = []
        for table_name in retrieved_tables_augmented:
            table_name_lower = table_name.lower()
            if table_name_lower in schema_dict:
                table_schemas_dict[table_name] = schema_dict[table_name_lower]
                table_names.append(table_name)
            else:
                # 如果找不到schema，跳过该表
                logger.info(f"⚠️  问题 {question_id} 表 {table_name} 的schema未找到")

        if not table_schemas_dict:
            skipped_questions.append({
                'question_id': question_id,
                'reason': '无有效表schema',
                'idx': idx
            })
            continue

        # 保存问题数据
        question_data_list.append({
            'question_id': question_id,
            'item': item,
            'query_text': query_text,
            'question': question,
            'ground_truth_tables': ground_truth_tables,
            'retrieved_tables_augmented': retrieved_tables_augmented,
            'table_schemas': table_schemas_dict,
            'table_names': table_names,
            'idx': idx
        })

    # 第二阶段：批量rerank
    logger.info(f"   准备rerank {len(question_data_list)} 个问题...")
    rerank_start_time = time.time()
    total_elapsed_time_ref = {'value': 0.0}  # 使用字典来避免nonlocal问题
    completed_count_ref = {'value': 0}  # 已完成问题计数器
    completed_count_lock = asyncio.Lock()  # 用于保护计数器的锁
    llm_score_count_issues_ref = {'issues': []}  # 记录LLM返回评分个数不是10的问题
    question_elapsed_times = []  # 收集所有问题的处理耗时（秒）

    async def process_single_question(qd: dict, semaphore: asyncio.Semaphore, rerank_results: list):
        """处理单个问题的rerank，完成后立即打印信息"""
        async with semaphore:
            question_start_time = time.time()
            question_id = qd['question_id']
            idx = qd['idx']

            try:
                # 使用LLM reranker异步调用
                response = await llm_reranker.rerank(
                    query=qd['query_text'],
                    schemas=qd['table_schemas']
                )

                # 处理LLM返回的结果
                # response.schema_list 是排序后的schema索引列表
                schema_list = response.schema_list
                schema_items = list(qd['table_schemas'].items())

                # 记录LLM返回schema个数不是10的问题
                llm_schema_count = len(schema_list)
                if llm_schema_count != 10:
                    llm_score_count_issues_ref['issues'].append({
                        'question_id': question_id,
                        'actual_count': llm_schema_count,
                        'expected_count': 10
                    })

                # 根据schema_list构建reranked_tables
                reranked_tables = []

                for schema_idx in schema_list:
                    if 0 <= schema_idx < len(schema_items):
                        table_name = schema_items[schema_idx][0]
                        reranked_tables.append(table_name)
                    else:
                        logger.info(f"   ⚠️  问题 {question_id}: LLM返回了无效的schema_index={schema_idx}，有效范围是0-{len(schema_items)-1}")

                # 对于LLM未返回的schema，添加到末尾
                matched_indices = {schema_idx for schema_idx in schema_list if 0 <= schema_idx < len(schema_items)}
                for idx, (table_name, _) in enumerate(schema_items):
                    if idx not in matched_indices:
                        reranked_tables.append(table_name)

                result = {
                    'question_data': qd,
                    'error': None,
                    'reranked_tables': reranked_tables
                }

                # 计算指标
                ground_truth_tables = qd['ground_truth_tables']
                map_score = calculate_map(reranked_tables, ground_truth_tables)

                # 计算耗时
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                # 更新完成计数器并获取当前完成数
                async with completed_count_lock:
                    completed_count_ref['value'] += 1
                    completed_count = completed_count_ref['value']

                # 立即打印问题信息
                num_tables_to_rerank = len(qd['table_schemas'])
                progress = (completed_count / len(question_data_list)) * 100
                logger.info(f"   [{progress:5.1f}%] 问题ID: {question_id} | 重排序表数: {num_tables_to_rerank} | 进度: {completed_count}/{len(question_data_list)} | MAP: {map_score:.4f} | 耗时: {question_elapsed_time:.2f}秒")

                rerank_results.append(result)

            except Exception as e:
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                # 更新完成计数器并获取当前完成数
                async with completed_count_lock:
                    completed_count_ref['value'] += 1
                    completed_count = completed_count_ref['value']

                progress = (completed_count / len(question_data_list)) * 100
                logger.info(f"   [{progress:5.1f}%] 问题ID: {question_id} | ⚠️  rerank失败: {e} | 进度: {completed_count}/{len(question_data_list)} | 耗时: {question_elapsed_time:.2f}秒")

                rerank_results.append({
                    'question_data': qd,
                    'error': e,
                    'reranked_tables': None
                })

    # 执行批量rerank
    rerank_results = []
    if reranker_type == "reranker_llm":
        # 使用异步批量处理
        semaphore = asyncio.Semaphore(40)
        tasks = [process_single_question(qd, semaphore, rerank_results) for qd in question_data_list]
        await asyncio.gather(*tasks)
    else:
        # 使用传统reranker逐个处理（同步）
        for processed_idx, qd in enumerate(question_data_list, 1):
            question_start_time = time.time()
            question_id = qd['question_id']
            idx = qd['idx']

            try:
                # 将字典转换为列表（保持顺序）
                schema_list = list(qd['table_schemas'].values())
                scores = rerank_schemas(qd['query_text'], schema_list, batch_size=batch_size)
                # 根据分数排序
                table_score_pairs = list(zip(qd['table_names'], scores))
                table_score_pairs.sort(key=lambda x: x[1], reverse=True)
                reranked_tables = [table for table, _ in table_score_pairs]

                # 计算指标
                ground_truth_tables = qd['ground_truth_tables']
                map_score = calculate_map(reranked_tables, ground_truth_tables)

                # 计算耗时
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                # 立即打印问题信息
                num_tables_to_rerank = len(qd['table_schemas'])
                progress = (processed_idx / len(question_data_list)) * 100
                logger.info(f"   [{progress:5.1f}%] 问题ID: {question_id} | 重排序表数: {num_tables_to_rerank} | 进度: {processed_idx}/{len(question_data_list)} | MAP: {map_score:.4f} | 耗时: {question_elapsed_time:.2f}秒")

                rerank_results.append({
                    'question_data': qd,
                    'error': None,
                    'reranked_tables': reranked_tables
                })
            except Exception as e:
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)
                progress = (processed_idx / len(question_data_list)) * 100
                logger.info(f"   [{progress:5.1f}%] 问题ID: {question_id} | ⚠️  rerank失败: {e} | 进度: {processed_idx}/{len(question_data_list)} | 耗时: {question_elapsed_time:.2f}秒")

                rerank_results.append({
                    'question_data': qd,
                    'error': e,
                    'reranked_tables': None
                })

    rerank_elapsed_time = time.time() - rerank_start_time
    logger.info(f"   批量rerank完成，总耗时: {rerank_elapsed_time:.2f}秒")

    # 第三阶段：处理结果并计算指标
    question_results = []
    map_scores = []
    recall_at_k_dict = {k: [] for k in k_list}
    precision_at_k_dict = {k: [] for k in k_list}
    f1_at_k_dict = {k: [] for k in k_list}

    # 处理被跳过的问题（打印跳过信息）
    for skipped in skipped_questions:
        progress = (skipped['idx'] / total_questions) * 100
        logger.info(f"   [{progress:5.1f}%] 问题ID: {skipped['question_id']} - 跳过（{skipped['reason']}） | 耗时: 0.00秒")

    # 处理rerank结果（不再打印，因为已经在第二阶段打印过了）
    for result in rerank_results:
        qd = result['question_data']
        question_id = qd['question_id']

        if result['error']:
            continue

        reranked_tables = result['reranked_tables']
        ground_truth_tables = qd['ground_truth_tables']

        # 计算指标
        map_score = calculate_map(reranked_tables, ground_truth_tables)
        map_scores.append(map_score)

        result_item = {
            'question_id': question_id,
            'db_id': qd['item'].get('db_id'),
            'question': qd['question'],
            'ground_truth_tables': sorted(list(ground_truth_tables)),
            'reranked_tables': reranked_tables,
            'metrics': {
                'map': map_score,
                'recall_at_k': {},
                'precision_at_k': {},
                'f1_at_k': {}
            },
            'retrieved_tables_augmented': qd['retrieved_tables_augmented']
        }

        for k in k_list:
            recall_k = calculate_recall_at_k(reranked_tables, ground_truth_tables, k)
            precision_k = calculate_precision_at_k(reranked_tables, ground_truth_tables, k)
            f1_k = calculate_f1_at_k(reranked_tables, ground_truth_tables, k)

            recall_at_k_dict[k].append(recall_k)
            precision_at_k_dict[k].append(precision_k)
            f1_at_k_dict[k].append(f1_k)

            result_item['metrics']['recall_at_k'][k] = recall_k
            result_item['metrics']['precision_at_k'][k] = precision_k
            result_item['metrics']['f1_at_k'][k] = f1_k

        question_results.append(result_item)

    # 计算平均指标
    avg_map = sum(map_scores) / len(map_scores) if map_scores else 0.0
    avg_recall_at_k = {
        k: sum(recall_at_k_dict[k]) / len(recall_at_k_dict[k])
        if len(recall_at_k_dict[k]) > 0 else 0.0
        for k in k_list
    }
    avg_precision_at_k = {
        k: sum(precision_at_k_dict[k]) / len(precision_at_k_dict[k])
        if len(precision_at_k_dict[k]) > 0 else 0.0
        for k in k_list
    }
    avg_f1_at_k = {
        k: sum(f1_at_k_dict[k]) / len(f1_at_k_dict[k])
        if len(f1_at_k_dict[k]) > 0 else 0.0
        for k in k_list
    }

    # 计算耗时统计信息
    latency_stats = calculate_latency_stats(question_elapsed_times)

    # 保存结果
    output_data = {
        'total_questions': total_questions,
        'valid_question_count': len(question_results),
        'reranker_type': reranker_type,
        'k_list': k_list,
        'metrics': {
            'map': avg_map,
            'recall_at_k': avg_recall_at_k,
            'precision_at_k': avg_precision_at_k,
            'f1_at_k': avg_f1_at_k
        },
        'latency': {
            'tp50': latency_stats['tp50'],
            'tp80': latency_stats['tp80'],
            'tp85': latency_stats['tp85'],
            'tp90': latency_stats['tp90'],
            'tp95': latency_stats['tp95'],
            'tp99': latency_stats['tp99'],
            'avg': latency_stats['avg'],
            'total': latency_stats['total'],
            'count': latency_stats['count']
        },
        'question_results': question_results
    }

    output_file = output_dir / 'rerank_eval_result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    logger.info("✅ Rerank评估完成！")
    logger.info(f"   有效问题数: {len(question_results)}")
    logger.info(f"   MAP: {avg_map:.4f}")
    for k in k_list:
        logger.info(f"   - Recall@{k}: {avg_recall_at_k[k]:.4f}")
    for k in k_list:
        logger.info(f"   * Precision@{k}: {avg_precision_at_k[k]:.4f}")
    for k in k_list:
        logger.info(f"   · F1@{k}: {avg_f1_at_k[k]:.4f}")
    logger.info(f"   耗时统计 - TP50: {latency_stats['tp50']:.2f}秒 | TP80: {latency_stats['tp80']:.2f}秒 | TP85: {latency_stats['tp85']:.2f}秒 | TP90: {latency_stats['tp90']:.2f}秒 | TP95: {latency_stats['tp95']:.2f}秒 | TP99: {latency_stats['tp99']:.2f}秒 | 平均: {latency_stats['avg']:.2f}秒")
    logger.info(f"   结果已保存到: {output_file}")

    # 收集MAP < 1且在top_k范围内未完全召回的问题
    # 使用k=10作为判断完全召回的标准（如果表排名在top 10以内则认为是完全召回）
    recall_check_k = 10
    incomplete_recall_issues = []
    for result in question_results:
        if result['metrics']['map'] < 1.0:
            recall_at_k = result['metrics']['recall_at_k']
            # 检查在top_k范围内是否完全召回
            if recall_at_k.get(recall_check_k, 1.0) < 1.0:
                tables_for_recall_one = calculate_tables_for_recall_one(
                    result['reranked_tables'],
                    set(result['ground_truth_tables'])
                )
                # 找出在top_k范围内没有召回的表及其排名
                top_k_tables = set(t.lower() for t in result['reranked_tables'][:recall_check_k])
                ground_truth_tables = set(t.lower() for t in result['ground_truth_tables'])
                missed_tables = ground_truth_tables - top_k_tables

                # 获取未召回表在reranked结果中的排名
                missed_tables_with_rank = []
                for i, table in enumerate(result['reranked_tables'], 1):
                    if table.lower() in missed_tables:
                        missed_tables_with_rank.append(f"{table}(排名{i})")

                incomplete_recall_issues.append({
                    'question_id': result['question_id'],
                    'tables_for_recall_one': tables_for_recall_one,
                    'recall_at_k': recall_at_k,
                    'missed_tables_with_rank': missed_tables_with_rank
                })

    if incomplete_recall_issues:
        logger.info(f"📋 Recall@{recall_check_k}没完全召回的问题:")
        for issue in incomplete_recall_issues:
            tables_info = f"需{issue['tables_for_recall_one']}个表" if issue['tables_for_recall_one'] > 0 else "无法达到recall=1"
            missed_tables_str = f"未召回: {issue['missed_tables_with_rank']}" if issue['missed_tables_with_rank'] else ""
            logger.info(f"   问题ID: {issue['question_id']} | {tables_info} | {missed_tables_str}")
    else:
        logger.info(f"📋 所有问题在Recall@{recall_check_k}都已完全召回")

    # 打印LLM返回评分个数统计（只显示MAP<1的问题）
    llm_score_count_issues = llm_score_count_issues_ref['issues']
    # 收集MAP<1的问题ID和MAP值映射
    map_less_than_one = {result['question_id']: result['metrics']['map'] for result in question_results if result['metrics']['map'] < 1.0}
    # 过滤出MAP<1且LLM返回评分个数不为10的问题
    filtered_issues = [issue for issue in llm_score_count_issues if issue['question_id'] in map_less_than_one]
    if filtered_issues:
        logger.info(f"📊 LLM返回评分个数不是10且MAP < 1的问题（共 {len(filtered_issues)}/{len(question_results)} 个）:")
        for issue in filtered_issues:
            map_score = map_less_than_one.get(issue['question_id'], 0.0)
            logger.info(f"   问题ID: {issue['question_id']} | MAP: {map_score:.4f} | 实际返回评分个数: {issue['actual_count']} (期望: {issue['expected_count']})")
    else:
        logger.info("📊 MAP<1的问题中，所有LLM返回评分个数均为10")


def main():
    parser = argparse.ArgumentParser(description='对检索结果进行rerank并计算评估指标')
    parser.add_argument(
        '--eval-results',
        type=str,
        default='src/pipeline/data/rereank/eval_results.json',
        help='评估结果文件路径'
    )
    parser.add_argument(
        '--schema',
        type=str,
        default='src/pipeline/output/rag_schema.sql',
        help='schema文件路径'
    )
    parser.add_argument(
        '--questions',
        type=str,
        default='src/pipeline/data/rereank/question_tables_extracted.json',
        help='问题文件路径'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='src/pipeline/output/rerank',
        help='输出目录'
    )
    parser.add_argument(
        '--k',
        type=int,
        nargs='+',
        default=[1, 3, 5, 10],
        help='K值列表'
    )
    parser.add_argument(
        '--reranker-type',
        type=str,
        choices=['reranker', 'reranker_llm'],
        default='reranker',
        help='reranker类型：reranker（使用Qwen3-Reranker模型）或 reranker_llm（使用LLM进行rerank，包含推理原因）'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=8,
        help='批次大小，用于控制内存使用，默认8。如果遇到CUDA内存不足，可以减小此值（如4或2）'
    )
    parser.add_argument(
        '--question-ids',
        type=str,
        help='问题ID列表文件路径（JSON格式），如果指定则只评估列表中的问题。'
    )

    args = parser.parse_args()

    question_ids_file = None
    if args.question_ids:
        question_ids_file = Path(args.question_ids)

    asyncio.run(evaluate_rerank(
        eval_results_file=Path(args.eval_results),
        schema_file=Path(args.schema),
        question_file=Path(args.questions),
        output_dir=Path(args.output),
        k_list=args.k,
        reranker_type=args.reranker_type,
        batch_size=args.batch_size,
        question_ids_file=question_ids_file
    ))


if __name__ == '__main__':
    main()
