"""Schema Linking benchmark测试

对SchemaProvider.schema_link进行性能评估，计算MAP指标
"""

import argparse
import asyncio
import json
import logging
import time
from pathlib import Path

from config import PROJECT_LOGGER_NAME
from context.schema_provider import SchemaProvider

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


def load_test_data(question_file: Path) -> list[dict]:
    """
    从测试数据文件加载问题列表

    Args:
        question_file: 测试数据文件路径

    Returns:
        问题数据列表
    """
    with open(question_file, encoding='utf-8') as f:
        return json.load(f)


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
    seen_relevant = set()

    for i, table in enumerate(retrieved_tables, 1):
        table_lower = table.lower()
        if table_lower in ground_truth_tables and table_lower not in seen_relevant:
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


async def evaluate_schema_link(
    question_file: Path,
    output_dir: Path,
    k_list: list[int] = [1, 3, 5, 10],
    concurrency: int = 1,
    database: str = "bird",
    stage: int = 3,
    question_ids_file: Path = None
) -> None:
    """
    对Schema Linking进行评估

    Args:
        question_file: 测试数据文件路径
        output_dir: 输出目录
        k_list: K值列表
        concurrency: 并发度，默认1（串行执行）
        database: 数据库名称
        stage: 执行阶段，1=仅阶段1，2=阶段1~2，3=全部阶段（默认3）
        question_ids_file: 问题ID列表文件路径，如果指定则只评估列表中的问题
    """
    stage_names = {1: "阶段1", 2: "阶段1~2", 3: "完整schema_link(3阶段)"}
    logger.info("📊 开始Schema Linking评估...")
    logger.info(f"   数据库: {database}")
    logger.info(f"   并发度: {concurrency}")
    logger.info(f"   执行阶段: {stage_names.get(stage, '未知')} (stage={stage})")

    # 初始化SchemaProvider
    schema_provider = SchemaProvider()

    # 加载测试数据
    logger.info("   加载测试数据...")
    test_data = load_test_data(question_file)
    logger.info(f"   已加载 {len(test_data)} 个测试问题")

    # 加载问题ID列表（如果指定）
    target_question_ids = None
    if question_ids_file:
        loaded_ids = load_question_ids(question_ids_file)
        if loaded_ids:
            target_question_ids = loaded_ids
            logger.info(f"   已加载 {len(target_question_ids)} 个指定问题ID，将只评估这些问题")
        else:
            logger.info("   ⚠️  问题ID文件为空或不存在，将评估所有问题")
            target_question_ids = None

    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)

    # 准备测试数据
    question_items = []
    for item in test_data:
        question_id = item.get('question_id')

        # 如果指定了问题ID列表，只处理列表中的问题
        if target_question_ids is not None and question_id not in target_question_ids:
            continue

        question = item.get('question', '')
        evidence = item.get('evidence', '')
        ground_truth_tables = set(t.lower() for t in item.get('ground_truth_tables', []))
        db_id = item.get('db_id', database)

        # 构建查询文本：question + evidence
        query_text = question
        if evidence:
            query_text = f"{question} {evidence}"

        question_items.append({
            'question_id': question_id,
            'query_text': query_text,
            'ground_truth_tables': ground_truth_tables,
            'db_id': db_id,
            'question': question,
            'evidence': evidence
        })

    # 过滤掉没有ground truth的问题
    valid_items = [item for item in question_items if item['ground_truth_tables']]
    skipped_count = len(question_items) - len(valid_items)
    if skipped_count > 0:
        logger.info(f"   跳过 {skipped_count} 个无ground truth的问题")

    # 执行评估
    logger.info(f"   准备评估 {len(valid_items)} 个问题...")
    benchmark_start_time = time.time()
    total_elapsed_time_ref = {'value': 0.0}
    completed_count_ref = {'value': 0}
    completed_count_lock = asyncio.Lock()
    question_elapsed_times = []

    async def process_single_question(
        item: dict,
        semaphore: asyncio.Semaphore,
        results: list
    ):
        """处理单个问题的Schema Linking"""
        async with semaphore:
            question_start_time = time.time()
            question_id = item['question_id']
            query_text = item['query_text']
            db_id = item['db_id']

            try:
                # 根据阶段执行不同的处理逻辑
                if stage == 1:
                    # 阶段1：仅向量检索
                    retrieved_tables, retrieved_tables_dict = await schema_provider._retrieve_from_vector_db(query_text, database)
                    matched_tables = retrieved_tables  # 取全部
                elif stage == 2:
                    # 阶段1+阶段2：向量检索 + RAG增强
                    retrieved_tables, retrieved_tables_dict = await schema_provider._retrieve_from_vector_db(query_text, database)
                    retrieved_tables, retrieved_tables_dict = schema_provider._rag_enhance(
                        retrieved_tables, retrieved_tables_dict, database
                    )
                    matched_tables = retrieved_tables  # 取全部
                else:
                    # stage 3：直接调用完整的schema_link方法
                    matched_tables, _ = await schema_provider.schema_link(query_text, database)

                # 计算耗时
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                # 计算指标
                ground_truth_tables = item['ground_truth_tables']
                map_score = calculate_map(matched_tables, ground_truth_tables)

                # 更新完成计数器
                async with completed_count_lock:
                    completed_count_ref['value'] += 1
                    completed_count = completed_count_ref['value']

                # 立即打印进度
                progress = (completed_count / len(valid_items)) * 100
                logger.info(
                    f"   [{progress:5.1f}%] 问题ID: {question_id} | "
                    f"匹配表数: {len(matched_tables)} | "
                    f"进度: {completed_count}/{len(valid_items)} | "
                    f"MAP: {map_score:.4f} | 耗时: {question_elapsed_time:.2f}秒"
                )

                results.append({
                    'question_id': question_id,
                    'db_id': db_id,
                    'question': item['question'],
                    'ground_truth_tables': sorted(list(ground_truth_tables)),
                    'matched_tables': matched_tables,
                    'map': map_score,
                    'error': None
                })

            except Exception as e:
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                # 更新完成计数器
                async with completed_count_lock:
                    completed_count_ref['value'] += 1
                    completed_count = completed_count_ref['value']

                progress = (completed_count / len(valid_items)) * 100
                logger.info(
                    f"   [{progress:5.1f}%] 问题ID: {question_id} | "
                    f"⚠️  Schema Link失败: {e} | "
                    f"进度: {completed_count}/{len(valid_items)} | "
                    f"耗时: {question_elapsed_time:.2f}秒"
                )

                results.append({
                    'question_id': question_id,
                    'db_id': db_id,
                    'question': item['question'],
                    'ground_truth_tables': sorted(list(item['ground_truth_tables'])),
                    'matched_tables': [],
                    'map': 0.0,
                    'error': str(e)
                })

    # 执行并发评估
    results = []
    if concurrency > 1:
        logger.info(f"   使用并发模式（并发度={concurrency}）...")
        semaphore = asyncio.Semaphore(concurrency)
        tasks = [process_single_question(item, semaphore, results) for item in valid_items]
        await asyncio.gather(*tasks)
    else:
        logger.info("   使用串行模式...")
        for processed_idx, item in enumerate(valid_items, 1):
            question_start_time = time.time()
            question_id = item['question_id']
            query_text = item['query_text']
            db_id = item['db_id']

            try:
                # 根据阶段执行不同的处理逻辑
                if stage == 1:
                    # 阶段1：仅向量检索
                    retrieved_tables, retrieved_tables_dict = await schema_provider._retrieve_from_vector_db(query_text, database)
                    matched_tables = retrieved_tables  # 取全部
                elif stage == 2:
                    # 阶段1+阶段2：向量检索 + RAG增强
                    retrieved_tables, retrieved_tables_dict = await schema_provider._retrieve_from_vector_db(query_text, database)
                    retrieved_tables, retrieved_tables_dict = schema_provider._rag_enhance(
                        retrieved_tables, retrieved_tables_dict, database
                    )
                    matched_tables = retrieved_tables  # 取全部
                else:
                    # stage 3：直接调用完整的schema_link方法
                    matched_tables, _ = await schema_provider.schema_link(query_text, database)

                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                ground_truth_tables = item['ground_truth_tables']
                map_score = calculate_map(matched_tables, ground_truth_tables)

                progress = (processed_idx / len(valid_items)) * 100
                logger.info(
                    f"   [{progress:5.1f}%] 问题ID: {question_id} | "
                    f"匹配表数: {len(matched_tables)} | "
                    f"进度: {processed_idx}/{len(valid_items)} | "
                    f"MAP: {map_score:.4f} | 耗时: {question_elapsed_time:.2f}秒"
                )

                results.append({
                    'question_id': question_id,
                    'db_id': db_id,
                    'question': item['question'],
                    'ground_truth_tables': sorted(list(ground_truth_tables)),
                    'matched_tables': matched_tables,
                    'map': map_score,
                    'error': None
                })

            except Exception as e:
                question_elapsed_time = time.time() - question_start_time
                total_elapsed_time_ref['value'] += question_elapsed_time
                question_elapsed_times.append(question_elapsed_time)

                progress = (processed_idx / len(valid_items)) * 100
                logger.info(
                    f"   [{progress:5.1f}%] 问题ID: {question_id} | "
                    f"⚠️  Schema Link失败: {e} | "
                    f"进度: {processed_idx}/{len(valid_items)} | "
                    f"耗时: {question_elapsed_time:.2f}秒"
                )

                results.append({
                    'question_id': question_id,
                    'db_id': db_id,
                    'question': item['question'],
                    'ground_truth_tables': sorted(list(item['ground_truth_tables'])),
                    'matched_tables': [],
                    'map': 0.0,
                    'error': str(e)
                })

    benchmark_elapsed_time = time.time() - benchmark_start_time
    logger.info(f"   批量评估完成，总耗时: {benchmark_elapsed_time:.2f}秒")

    # 计算整体指标
    valid_results = [r for r in results if r['error'] is None]
    error_count = len(results) - len(valid_results)

    map_scores = [r['map'] for r in valid_results]
    recall_at_k_dict = {k: [] for k in k_list}
    precision_at_k_dict = {k: [] for k in k_list}
    f1_at_k_dict = {k: [] for k in k_list}

    for result in valid_results:
        matched_tables = result['matched_tables']
        ground_truth_tables = set(t.lower() for t in result['ground_truth_tables'])

        for k in k_list:
            recall_k = calculate_recall_at_k(matched_tables, ground_truth_tables, k)
            precision_k = calculate_precision_at_k(matched_tables, ground_truth_tables, k)
            f1_k = calculate_f1_at_k(matched_tables, ground_truth_tables, k)

            recall_at_k_dict[k].append(recall_k)
            precision_at_k_dict[k].append(precision_k)
            f1_at_k_dict[k].append(f1_k)

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
        'total_questions': len(valid_items),
        'valid_question_count': len(valid_results),
        'error_count': error_count,
        'database': database,
        'concurrency': concurrency,
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
        'results': results
    }

    output_file = output_dir / 'schema_link_eval_result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    # 打印评估结果
    logger.info("✅ Schema Linking评估完成！")
    logger.info(f"   总问题数: {len(valid_items)}")
    logger.info(f"   有效评估: {len(valid_results)}")
    logger.info(f"   失败: {error_count}")
    logger.info(f"   MAP: {avg_map:.4f}")
    for k in k_list:
        logger.info(f"   - Recall@{k}: {avg_recall_at_k[k]:.4f}")
    for k in k_list:
        logger.info(f"   * Precision@{k}: {avg_precision_at_k[k]:.4f}")
    for k in k_list:
        logger.info(f"   · F1@{k}: {avg_f1_at_k[k]:.4f}")
    logger.info(
        f"   耗时统计 - "
        f"TP50: {latency_stats['tp50']:.2f}秒 | "
        f"TP80: {latency_stats['tp80']:.2f}秒 | "
        f"TP90: {latency_stats['tp90']:.2f}秒 | "
        f"TP95: {latency_stats['tp95']:.2f}秒 | "
        f"TP99: {latency_stats['tp99']:.2f}秒 | "
        f"平均: {latency_stats['avg']:.2f}秒"
    )
    logger.info(f"   结果已保存到: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='Schema Linking benchmark测试')
    parser.add_argument(
        '--questions',
        type=str,
        default='src/pipeline/data/rereank/question_tables_extracted.json',
        help='测试数据文件路径'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='src/pipeline/output/schema_link',
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
        '--concurrency',
        type=int,
        default=1,
        help='并发度，默认1（串行执行）。大于1时启用并发模式'
    )
    parser.add_argument(
        '--database',
        type=str,
        default='bird',
        help='数据库名称，默认bird'
    )
    parser.add_argument(
        '--stage',
        type=int,
        default=3,
        choices=[1, 2, 3],
        help='执行阶段：1=仅阶段1（向量检索），2=阶段1~2（向量检索+RAG增强），3=完整schema_link（含Rerank），默认3'
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

    asyncio.run(evaluate_schema_link(
        question_file=Path(args.questions),
        output_dir=Path(args.output),
        k_list=args.k,
        concurrency=args.concurrency,
        database=args.database,
        stage=args.stage,
        question_ids_file=question_ids_file
    ))


if __name__ == '__main__':
    main()
