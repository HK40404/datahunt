import argparse
import asyncio
import json
from pathlib import Path

from context.table_relation_provider import TableRelationProvider
from embed.bge_embedder import BGEEmbedder
from graph.rewritter import QueryRewritter
from llm.openai import openai_client
from vectordb.milvus import MilvusWrapper


async def evaluate_rag_performance(
    questions_file: str | Path,
    collection_name: str = "bird",
    database: str = "bird",
    top_k_list: list[int] = [1, 3, 5, 10],
    beta: float = 1.0,
    use_hybrid_search: bool = True,
    use_evidence: bool = False,
    use_rewrite: bool = False,
    rewrite_output_file: str | Path | None = None,
    rag_augmented: bool = False,
    hops: int = 1,
    total_limit: int | None = None,
    single_limit: int | None = None
) -> dict:
    """
    评估RAG性能：使用question embedding查询DDL数据，计算召回率、Precision@K、F-β值

    Args:
        questions_file: 包含问题和表名的JSON文件路径
        collection_name: Milvus collection名称
        database: 数据库名称，用于过滤metadata
        top_k_list: 要计算的Precision@K的K值列表
        beta: F-β值中的β参数（β=1时为F1，β=2时更重视召回率，β=0.5时更重视精确率）
        use_hybrid_search: 是否使用混合检索（稠密+稀疏向量）
        use_evidence: 是否使用question+evidence作为查询文本（默认只使用question）
        use_rewrite: 是否使用QueryRewritter改写问题（改写后的query作为查询文本）
        rewrite_output_file: 改写结果保存路径（JSON格式），包含question_id、question、evidence、rewritted_query
        rag_augmented: 是否启用RAG增强，将top-k个表在N hop内的关联表也加入检索结果
        hops: RAG增强时的跳数（默认1）
        total_limit: 获取关联表时限制返回的关联表总数量，None表示不限制
        single_limit: 获取关联表时单个源表最多返回的关联表数量，None表示不限制

    Returns:
        包含评估结果的字典
    """
    # 加载问题数据
    questions_path = Path(questions_file)
    if not questions_path.exists():
        raise FileNotFoundError(f"文件不存在: {questions_path}")

    with open(questions_path, encoding='utf-8') as f:
        questions_data = json.load(f)

    print("📊 开始评估RAG性能...")
    print(f"   问题数量: {len(questions_data)}")
    print(f"   Collection: {collection_name}")
    print(f"   Database: {database}")
    print(f"   混合检索: {use_hybrid_search}")
    print(f"   使用Evidence: {use_evidence}")
    print(f"   使用Rewrite: {use_rewrite}")
    print(f"   RAG增强: {rag_augmented}")
    if rag_augmented:
        max_k = max(top_k_list) if top_k_list else 10
        print(f"   检索返回表数: {max_k}")
        print(f"   关联表跳数: {hops}")
        if total_limit is not None:
            print(f"   关联表总数限制: {total_limit}")
        if single_limit is not None:
            print(f"   单个源表关联表限制: {single_limit}")
    print(f"   β值: {beta}")

    # 初始化embedder和milvus
    embedder = BGEEmbedder()
    milvus = MilvusWrapper(
        collection_name=collection_name,
        dimension=1024,  # BGE-M3的维度
        auto_create=False
    )

    if not milvus.collection_exists():
        raise ValueError(f"Collection '{collection_name}' 不存在，请先运行 ddl_embed.py")

    # 如果使用rewrite，初始化QueryRewritter
    rewriter = None
    if use_rewrite:
        rewriter = QueryRewritter(client=openai_client)
        print("   QueryRewritter已初始化")

    # 如果使用RAG增强，初始化TableRelationProvider
    relation_provider = None
    if rag_augmented:
        try:
            relation_provider = TableRelationProvider()
            print("   TableRelationProvider已初始化")
        except Exception as e:
            print(f"⚠️  TableRelationProvider初始化失败: {e}")
            print("   将禁用RAG增强功能")
            rag_augmented = False

    # 存储改写结果
    rewrite_results = []

    # 统计信息
    total_questions = len(questions_data)
    max_k = max(top_k_list) if top_k_list else 10

    # 存储每个问题的评估结果
    question_results = []

    # 存储每个问题的 Average Precision (用于计算 MAP)
    average_precision_list_original = []
    average_precision_list_augmented = []

    # 总体统计 - 原始指标（不使用关联表）
    total_recall_original = 0.0
    precision_at_k_dict_original = {k: [] for k in top_k_list}
    recall_at_k_dict_original = {k: [] for k in top_k_list}
    f_beta_dict_original = {k: [] for k in top_k_list}
    # 存储分子和分母用于显示
    recall_at_k_numerator_original = {k: [] for k in top_k_list}  # 相关表数量
    recall_at_k_denominator_original = {k: [] for k in top_k_list}  # ground truth表总数
    precision_at_k_numerator_original = {k: [] for k in top_k_list}  # 相关表数量
    precision_at_k_denominator_original = {k: [] for k in top_k_list}  # 检索结果数或检索到的表数

    # 总体统计 - 增强后指标（使用关联表，仅在rag_augmented=True时计算）
    total_recall_augmented = 0.0
    precision_at_k_dict_augmented = {k: [] for k in top_k_list}
    recall_at_k_dict_augmented = {k: [] for k in top_k_list}
    f_beta_dict_augmented = {k: [] for k in top_k_list}
    # 存储分子和分母用于显示
    recall_at_k_numerator_augmented = {k: [] for k in top_k_list}  # 相关表数量
    recall_at_k_denominator_augmented = {k: [] for k in top_k_list}  # ground truth表总数
    precision_at_k_numerator_augmented = {k: [] for k in top_k_list}  # 相关表数量
    precision_at_k_denominator_augmented = {k: [] for k in top_k_list}  # 检索到的表数（包含关联表）

    valid_question_count = 0

    # 如果使用rewrite，先批量改写所有问题
    rewrite_map = {}  # 存储 question_id -> rewritted_query 的映射
    if use_rewrite and rewriter:
        # 收集所有需要改写的问题
        rewrite_requests = []
        rewrite_indices = []  # 记录每个请求对应的item索引和question_id
        for idx, item in enumerate(questions_data):
            question = item.get('question', '')
            evidence = item.get('evidence', '')
            ground_truth_tables = set(t.lower() for t in item.get('ground_truth_tables', []))
            question_id = item.get('question_id')

            # 跳过没有ground truth表的问题
            if not ground_truth_tables:
                continue

            rewrite_requests.append((question, evidence))
            rewrite_indices.append((idx, question_id))

        # 批量改写
        if rewrite_requests:
            print(f"   开始批量改写 {len(rewrite_requests)} 个问题...")
            batch_results = await rewriter.batch_rewrite(rewrite_requests, max_concurrent=10)

            # 处理批量改写结果
            for (idx, question_id), (rewrite_response, error) in zip(rewrite_indices, batch_results):
                item = questions_data[idx]
                question = item.get('question', '')
                evidence = item.get('evidence', '')

                if error:
                    print(f"⚠️  问题 {question_id} 改写失败: {error}")
                    rewrite_map[question_id] = None  # None表示改写失败，使用原始问题
                else:
                    rewritted_query = rewrite_response.query
                    rewrite_map[question_id] = rewritted_query

                    # 保存改写结果
                    rewrite_results.append({
                        'question_id': question_id,
                        'question': question,
                        'evidence': evidence,
                        'rewritted_query': rewritted_query,
                        'reasoning': rewrite_response.reasoning
                    })
            print(f"   批量改写完成，成功 {len([r for r in rewrite_map.values() if r is not None])} 个，失败 {len([r for r in rewrite_map.values() if r is None])} 个")

    # 处理每个问题
    for idx, item in enumerate(questions_data, 1):
        question = item.get('question', '')
        evidence = item.get('evidence', '')
        ground_truth_tables = set(t.lower() for t in item.get('ground_truth_tables', []))
        question_id = item.get('question_id')
        db_id = item.get('db_id')

        # 跳过没有ground truth表的问题
        if not ground_truth_tables:
            continue

        valid_question_count += 1

        # 构建查询文本
        rewritted_query = None
        if use_rewrite and rewriter:
            # 使用批量改写的结果
            rewritted_query = rewrite_map.get(question_id)
            if rewritted_query:
                query_text = rewritted_query
            else:
                # 改写失败时回退到原始问题
                query_text = question
        elif use_evidence and evidence:
            # 如果use_evidence为True，则使用question+evidence
            query_text = f"{question} {evidence}"
        else:
            query_text = question

        # 对查询文本进行embedding
        query_dense_vector = embedder.embed_texts_dense([query_text])[0]
        query_sparse_vector = embedder.embed_texts_sparse([query_text])[0] if use_hybrid_search else None

        # 查询Milvus（只查询指定数据库的数据）
        filter_expr = f'metadata["database"] == "{database}"'

        if use_hybrid_search and query_sparse_vector:
            search_results = milvus.search_by_vector(
                query_vector=query_dense_vector,
                query_sparse_vector=query_sparse_vector,
                top_k=max_k,
                filter=filter_expr
            )
        else:
            search_results = milvus.search_by_vector(
                query_vector=query_dense_vector,
                top_k=max_k,
                filter=filter_expr
            )

        # 提取检索结果中的表名（从所有检索结果中提取，保持相关性顺序）
        # 使用 dict 的 key 作为有序 set，自动去重并保持顺序
        retrieved_tables_dict = {}
        for result in search_results:
            metadata = result.get('metadata', {})
            table_name = metadata.get('table_name', '').lower()
            if table_name and table_name != 'unknown':
                retrieved_tables_dict[table_name] = None  # 使用 dict key 作为有序 set

        retrieved_tables_original = set(retrieved_tables_dict.keys())

        # 如果启用RAG增强，将检索到的表的关联表也加入
        retrieved_tables_augmented = set(retrieved_tables_dict.keys())
        if rag_augmented and relation_provider:
            # 获取所有检索到的表中在关系图中存在的表
            tables_in_graph = [t for t in retrieved_tables_dict.keys() if relation_provider.has_table(t)]
            if tables_in_graph:
                try:
                    # 获取这些表的关联表
                    related_tables = relation_provider.get_connected_tables(
                        tables_in_graph,
                        max_hops=hops,
                        total_limit=total_limit,
                        single_limit=single_limit
                    )
                    retrieved_tables_augmented.update(related_tables)
                except Exception as e:
                    print(f"⚠️  问题 {question_id} 获取关联表失败: {e}")

        # ========== 1. 召回率（Recall）计算 ==========
        # 召回率 = 检索到的相关表数量 / 真实相关的表总数
        #
        # 示例：
        #   - Ground Truth: ['customers', 'orders', 'products'] (3个表)
        #   - 检索结果: ['customers', 'orders', 'items', 'users'] (检索到4个表)
        #   - 相关表: ['customers', 'orders'] (2个在ground truth中)
        #   - Recall = 2 / 3 = 0.667 (66.7%的相关表被检索到了)
        #
        # 注意：召回率基于所有检索结果（top_k=max_k），不受K值限制

        # 计算原始召回率（不使用关联表）
        if ground_truth_tables:
            recall_original = len(retrieved_tables_original & ground_truth_tables) / len(ground_truth_tables)
        else:
            recall_original = 0.0

        total_recall_original += recall_original

        # 计算增强后召回率（使用关联表，仅在rag_augmented=True时计算）
        recall_augmented = None
        if rag_augmented:
            if ground_truth_tables:
                recall_augmented = len(retrieved_tables_augmented & ground_truth_tables) / len(ground_truth_tables)
            else:
                recall_augmented = 0.0
            total_recall_augmented += recall_augmented

        # ========== 2. Precision@K 和 F-β@K 计算 ==========
        result_item = {
            'question_id': question_id,
            'db_id': db_id,
            'ground_truth_tables': sorted(list(ground_truth_tables)),
            'retrieved_tables': list(retrieved_tables_dict.keys()),  # 保持相关性顺序，不按字母排序
            'metrics_original': {
                'recall': recall_original,
                'recall_at_k': {},
                'precision_at_k': {},
                'f_beta': {}
            }
        }

        # 如果启用RAG增强，添加增强后的指标和检索表
        if rag_augmented:
            # 构建增强后的表列表：先保存原始检索的表（保持顺序），然后添加关联表（保持get_connected_tables返回顺序）
            retrieved_tables_augmented_list = list(retrieved_tables_dict.keys())  # 原始检索的表，保持顺序
            related_tables_only = retrieved_tables_augmented - retrieved_tables_original  # 只包含关联表
            if related_tables_only:
                # 按get_connected_tables返回的顺序添加关联表，保持与schema_provider._rag_enhance一致
                for related_table in related_tables:
                    if related_table in related_tables_only:
                        retrieved_tables_augmented_list.append(related_table)
            result_item['retrieved_tables_augmented'] = retrieved_tables_augmented_list

            result_item['metrics_augmented'] = {
                'recall': recall_augmented,
                'recall_at_k': {},
                'precision_at_k': {},
                'f_beta': {}
            }

        # 计算未召回的表（只在召回率低于100%时添加）
        if recall_original < 1.0:
            miss_tables_original = ground_truth_tables - retrieved_tables_original
            if miss_tables_original:
                result_item['metrics_original']['miss_tables'] = sorted(list(miss_tables_original))

        if rag_augmented and recall_augmented is not None and recall_augmented < 1.0:
            miss_tables_augmented = ground_truth_tables - retrieved_tables_augmented
            if miss_tables_augmented:
                result_item['metrics_augmented']['miss_tables'] = sorted(list(miss_tables_augmented))

        for k in top_k_list:
            # 取前k个检索结果
            top_k_results = search_results[:k]
            # 使用 dict 的 key 作为有序 set，自动去重并保持顺序
            top_k_tables_dict = {}
            for result in top_k_results:
                metadata = result.get('metadata', {})
                table_name = metadata.get('table_name', '').lower()
                if table_name and table_name != 'unknown':
                    top_k_tables_dict[table_name] = None  # 使用 dict key 作为有序 set

            # 原始指标：不使用关联表
            top_k_tables_original = set(top_k_tables_dict.keys())

            # 增强后指标：将top-k个表的关联表也加入
            top_k_tables_augmented = set(top_k_tables_dict.keys())
            if rag_augmented and relation_provider:
                # 获取top-k个表中在关系图中存在的表
                top_k_tables_in_graph = [t for t in top_k_tables_dict.keys() if relation_provider.has_table(t)]
                if top_k_tables_in_graph:
                    try:
                        # 获取这些表的关联表
                        related_tables = relation_provider.get_connected_tables(
                            top_k_tables_in_graph,
                            max_hops=hops,
                            total_limit=total_limit,
                            single_limit=single_limit
                        )
                        top_k_tables_augmented.update(related_tables)
                    except Exception as e:
                        print(f"⚠️  问题 {question_id} K={k} 获取关联表失败: {e}")

            # ========== Recall@K 计算 ==========
            # Recall@K = 前K个结果中相关表的数量 / 真实相关的表总数
            #
            # 示例（K=5）：
            #   - Ground Truth: ['customers', 'orders', 'products'] (3个表)
            #   - 前5个检索结果: ['customers', 'orders', 'items', 'users']
            #   - 相关表: ['customers', 'orders'] (2个在ground truth中)
            #   - Recall@5 = 2 / 3 = 0.667 (前5个结果中找到了66.7%的相关表)
            #
            # 注意：Recall@K 基于前K个检索结果，分母是ground truth表的数量

            # 计算原始Recall@K（不使用关联表）
            if ground_truth_tables:
                recall_numerator_original = len(top_k_tables_original & ground_truth_tables)
                recall_denominator_original = len(ground_truth_tables)
                recall_at_k_original = recall_numerator_original / recall_denominator_original
            else:
                recall_numerator_original = 0
                recall_denominator_original = 0
                recall_at_k_original = 0.0
            recall_at_k_dict_original[k].append(recall_at_k_original)
            recall_at_k_numerator_original[k].append(recall_numerator_original)
            recall_at_k_denominator_original[k].append(recall_denominator_original)
            result_item['metrics_original']['recall_at_k'][k] = recall_at_k_original

            # 计算增强后Recall@K（使用关联表，仅在rag_augmented=True时计算）
            if rag_augmented:
                if ground_truth_tables:
                    recall_numerator_augmented = len(top_k_tables_augmented & ground_truth_tables)
                    recall_denominator_augmented = len(ground_truth_tables)
                    recall_at_k_augmented = recall_numerator_augmented / recall_denominator_augmented
                else:
                    recall_numerator_augmented = 0
                    recall_denominator_augmented = 0
                    recall_at_k_augmented = 0.0
                recall_at_k_dict_augmented[k].append(recall_at_k_augmented)
                recall_at_k_numerator_augmented[k].append(recall_numerator_augmented)
                recall_at_k_denominator_augmented[k].append(recall_denominator_augmented)
                result_item['metrics_augmented']['recall_at_k'][k] = recall_at_k_augmented

            # ========== Precision@K 计算 ==========
            # Precision@K = 前K个结果中相关表的数量 / K
            #
            # 示例（K=5）：
            #   - Ground Truth: ['customers', 'orders', 'products'] (3个表)
            #   - 前5个检索结果: ['customers', 'orders', 'items', 'users', 'products']
            #   - 相关表: ['customers', 'orders', 'products'] (3个在ground truth中)
            #   - Precision@5 = 3 / 5 = 0.6 (前5个结果中60%是相关的)
            #
            # 注意：K是检索结果数量，不是相关表的数量

            # 计算原始Precision@K（不使用关联表）
            # 分母是 k（检索结果数量），分子是相关表的数量
            precision_numerator_original = len(top_k_tables_original & ground_truth_tables)
            precision_denominator_original = k
            precision_at_k_original = precision_numerator_original / precision_denominator_original if precision_denominator_original > 0 else 0.0
            precision_at_k_dict_original[k].append(precision_at_k_original)
            precision_at_k_numerator_original[k].append(precision_numerator_original)
            precision_at_k_denominator_original[k].append(precision_denominator_original)
            result_item['metrics_original']['precision_at_k'][k] = precision_at_k_original

            # 计算增强后Precision@K（使用关联表，仅在rag_augmented=True时计算）
            # 注意：由于添加了关联表，相关表的数量可能超过 k
            # 为了保持 Precision 在 [0, 1] 范围内，分母使用实际检索到的表数量（包含关联表）
            if rag_augmented:
                # 实际检索到的表数量（包含关联表）
                total_retrieved_tables = len(top_k_tables_augmented)
                precision_numerator_augmented = len(top_k_tables_augmented & ground_truth_tables)
                precision_denominator_augmented = total_retrieved_tables
                precision_at_k_augmented = precision_numerator_augmented / precision_denominator_augmented if precision_denominator_augmented > 0 else 0.0
                precision_at_k_dict_augmented[k].append(precision_at_k_augmented)
                precision_at_k_numerator_augmented[k].append(precision_numerator_augmented)
                precision_at_k_denominator_augmented[k].append(precision_denominator_augmented)
                result_item['metrics_augmented']['precision_at_k'][k] = precision_at_k_augmented

            # ========== F-β@K 计算 ==========
            # F-β@K = (1 + β²) * (Precision@K * Recall@K) / (β² * Precision@K + Recall@K)
            #
            # β值含义：
            #   - β = 1: F1分数，精确率和召回率同等重要
            #   - β > 1: 更重视召回率（如β=2时，召回率权重是精确率的4倍）
            #   - β < 1: 更重视精确率（如β=0.5时，精确率权重是召回率的4倍）
            #
            # 注意：这里使用Precision@K和Recall@K计算F-β@K

            # 计算原始F-β@K
            if precision_at_k_original + recall_at_k_original > 0:
                f_beta_k_original = (1 + beta ** 2) * (precision_at_k_original * recall_at_k_original) / (beta ** 2 * precision_at_k_original + recall_at_k_original)
            else:
                f_beta_k_original = 0.0

            f_beta_dict_original[k].append(f_beta_k_original)
            result_item['metrics_original']['f_beta'][k] = f_beta_k_original

            # 计算增强后F-β@K（仅在rag_augmented=True时计算）
            if rag_augmented:
                if precision_at_k_augmented + recall_at_k_augmented > 0:
                    f_beta_k_augmented = (1 + beta ** 2) * (precision_at_k_augmented * recall_at_k_augmented) / (beta ** 2 * precision_at_k_augmented + recall_at_k_augmented)
                else:
                    f_beta_k_augmented = 0.0

                f_beta_dict_augmented[k].append(f_beta_k_augmented)
                result_item['metrics_augmented']['f_beta'][k] = f_beta_k_augmented

        # ========== 4. 计算 Average Precision (AP) ==========
        # AP = (1/R) * ∑(Precision@i * rel_i)，其中 rel_i = 1 如果位置i的结果是相关的
        # R = 真实相关表总数
        #
        # AP 衡量检索结果排序的质量，考虑每个相关文档出现的位置
        # 理想情况下，所有相关文档都排在前面，AP 接近 1.0
        # 如果相关文档排在后面，AP 会降低

        # 原始指标的 AP（不使用关联表）
        retrieved_list_original = list(retrieved_tables_dict.keys())  # 按相关性排序的检索结果
        ap_original = 0.0
        num_relevant_original = 0
        for i, table in enumerate(retrieved_list_original, 1):  # i 从 1 开始
            if table in ground_truth_tables:
                # Precision@i = 前面i个结果中相关的数量 / i
                # 这里用已找到的相关表数量 / i
                num_relevant_original += 1
                precision_at_i = num_relevant_original / i
                ap_original += precision_at_i

        if len(ground_truth_tables) > 0:
            ap_original = ap_original / len(ground_truth_tables)
        else:
            ap_original = 0.0

        average_precision_list_original.append(ap_original)
        result_item['metrics_original']['average_precision'] = ap_original

        # 增强后指标的 AP（使用关联表，仅在 rag_augmented=True 时计算）
        ap_augmented = None
        if rag_augmented:
            # 增强后的检索列表（原始检索表保持顺序，关联表追加）
            retrieved_list_augmented = result_item.get('retrieved_tables_augmented', [])
            ap_augmented = 0.0
            num_relevant_augmented = 0
            for i, table in enumerate(retrieved_list_augmented, 1):
                if table in ground_truth_tables:
                    num_relevant_augmented += 1
                    precision_at_i = num_relevant_augmented / i
                    ap_augmented += precision_at_i

            if len(ground_truth_tables) > 0:
                ap_augmented = ap_augmented / len(ground_truth_tables)
            else:
                ap_augmented = 0.0

            average_precision_list_augmented.append(ap_augmented)
            result_item['metrics_augmented']['average_precision'] = ap_augmented

        question_results.append(result_item)

        # 显示进度
        if idx % 50 == 0:
            print(f"   已处理: {idx}/{total_questions}")

    # ========== 3. 计算平均指标 ==========
    # 对所有有效问题（有ground truth表的问题）的指标求平均值

    # 原始指标的平均值
    avg_recall_original = total_recall_original / valid_question_count if valid_question_count > 0 else 0.0
    avg_recall_at_k_original = {
        k: sum(recall_at_k_dict_original[k]) / len(recall_at_k_dict_original[k])
        if len(recall_at_k_dict_original[k]) > 0 else 0.0
        for k in top_k_list
    }
    avg_precision_at_k_original = {
        k: sum(precision_at_k_dict_original[k]) / len(precision_at_k_dict_original[k])
        if len(precision_at_k_dict_original[k]) > 0 else 0.0
        for k in top_k_list
    }
    avg_f_beta_original = {
        k: sum(f_beta_dict_original[k]) / len(f_beta_dict_original[k])
        if len(f_beta_dict_original[k]) > 0 else 0.0
        for k in top_k_list
    }
    # 计算 MAP (Mean Average Precision)
    map_original = sum(average_precision_list_original) / len(average_precision_list_original) if len(average_precision_list_original) > 0 else 0.0

    # 计算平均分子和分母
    avg_recall_at_k_numerator_original = {
        k: sum(recall_at_k_numerator_original[k]) / len(recall_at_k_numerator_original[k])
        if len(recall_at_k_numerator_original[k]) > 0 else 0.0
        for k in top_k_list
    }
    avg_recall_at_k_denominator_original = {
        k: sum(recall_at_k_denominator_original[k]) / len(recall_at_k_denominator_original[k])
        if len(recall_at_k_denominator_original[k]) > 0 else 0.0
        for k in top_k_list
    }
    avg_precision_at_k_numerator_original = {
        k: sum(precision_at_k_numerator_original[k]) / len(precision_at_k_numerator_original[k])
        if len(precision_at_k_numerator_original[k]) > 0 else 0.0
        for k in top_k_list
    }
    avg_precision_at_k_denominator_original = {
        k: sum(precision_at_k_denominator_original[k]) / len(precision_at_k_denominator_original[k])
        if len(precision_at_k_denominator_original[k]) > 0 else 0.0
        for k in top_k_list
    }

    # 增强后指标的平均值（仅在rag_augmented=True时计算）
    avg_recall_augmented = None
    avg_recall_at_k_augmented = None
    avg_precision_at_k_augmented = None
    avg_f_beta_augmented = None
    map_augmented = None  # 增强后的 MAP
    avg_recall_at_k_numerator_augmented = None
    avg_recall_at_k_denominator_augmented = None
    avg_precision_at_k_numerator_augmented = None
    avg_precision_at_k_denominator_augmented = None

    if rag_augmented:
        avg_recall_augmented = total_recall_augmented / valid_question_count if valid_question_count > 0 else 0.0
        avg_recall_at_k_augmented = {
            k: sum(recall_at_k_dict_augmented[k]) / len(recall_at_k_dict_augmented[k])
            if len(recall_at_k_dict_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }
        avg_precision_at_k_augmented = {
            k: sum(precision_at_k_dict_augmented[k]) / len(precision_at_k_dict_augmented[k])
            if len(precision_at_k_dict_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }
        avg_f_beta_augmented = {
            k: sum(f_beta_dict_augmented[k]) / len(f_beta_dict_augmented[k])
            if len(f_beta_dict_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }
        # 计算增强后的 MAP (Mean Average Precision)
        map_augmented = sum(average_precision_list_augmented) / len(average_precision_list_augmented) if len(average_precision_list_augmented) > 0 else 0.0
        # 计算平均分子和分母
        avg_recall_at_k_numerator_augmented = {
            k: sum(recall_at_k_numerator_augmented[k]) / len(recall_at_k_numerator_augmented[k])
            if len(recall_at_k_numerator_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }
        avg_recall_at_k_denominator_augmented = {
            k: sum(recall_at_k_denominator_augmented[k]) / len(recall_at_k_denominator_augmented[k])
            if len(recall_at_k_denominator_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }
        avg_precision_at_k_numerator_augmented = {
            k: sum(precision_at_k_numerator_augmented[k]) / len(precision_at_k_numerator_augmented[k])
            if len(precision_at_k_numerator_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }
        avg_precision_at_k_denominator_augmented = {
            k: sum(precision_at_k_denominator_augmented[k]) / len(precision_at_k_denominator_augmented[k])
            if len(precision_at_k_denominator_augmented[k]) > 0 else 0.0
            for k in top_k_list
        }

    # 保存改写结果
    if use_rewrite and rewrite_output_file and rewrite_results:
        rewrite_output_path = Path(rewrite_output_file)
        rewrite_output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(rewrite_output_path, 'w', encoding='utf-8') as f:
            json.dump(rewrite_results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 改写结果已保存到: {rewrite_output_path.absolute()}")
        print(f"   共改写 {len(rewrite_results)} 个问题")

    # 汇总结果
    evaluation_results = {
        'total_questions': total_questions,
        'valid_question_count': valid_question_count,
        'collection_name': collection_name,
        'database': database,
        'use_hybrid_search': use_hybrid_search,
        'use_evidence': use_evidence,
        'use_rewrite': use_rewrite,
        'rag_augmented': rag_augmented,
        'hops': hops if rag_augmented else None,
        'beta': beta,
        'metrics_original': {
            'recall': avg_recall_original,
            'recall_at_k': avg_recall_at_k_original,
            'precision_at_k': avg_precision_at_k_original,
            'f_beta': avg_f_beta_original,
            'map': map_original
        },
        'question_results': question_results
    }

    # 如果启用RAG增强，添加增强后的指标
    if rag_augmented:
        evaluation_results['metrics_augmented'] = {
            'recall': avg_recall_augmented,
            'recall_at_k': avg_recall_at_k_augmented,
            'precision_at_k': avg_precision_at_k_augmented,
            'f_beta': avg_f_beta_augmented,
            'map': map_augmented
        }

    # 打印结果
    print("\n✅ 评估完成！")
    print("\n📊 评估结果:")
    print(f"   总问题数: {total_questions}")
    print(f"   有效问题数（有ground truth表）: {valid_question_count}")

    # 打印原始指标
    print("\n📈 原始指标（不使用关联表）:")
    print(f"   平均召回率: {avg_recall_original:.4f}")
    print("\n   Recall@K:")
    for k in top_k_list:
        num = avg_recall_at_k_numerator_original[k]
        den = avg_recall_at_k_denominator_original[k]
        print(f"     Recall@{k}: {avg_recall_at_k_original[k]:.4f} (平均召回: {num:.2f}, 平均GT: {den:.2f})")
    print("\n   Precision@K:")
    for k in top_k_list:
        num = avg_precision_at_k_numerator_original[k]
        den = avg_precision_at_k_denominator_original[k]
        print(f"     Precision@{k}: {avg_precision_at_k_original[k]:.4f} (平均相关: {num:.2f}, 平均检索: {den:.2f})")
    print(f"\n   F-{beta}@K:")
    for k in top_k_list:
        print(f"     F-{beta}@{k}: {avg_f_beta_original[k]:.4f}")
    print(f"\n   MAP: {map_original:.4f}")

    # 如果启用RAG增强，打印增强后的指标
    if rag_augmented:
        print(f"\n📈 增强后指标（使用关联表，hops={hops}）:")
        print(f"   平均召回率: {avg_recall_augmented:.4f}")
        print("\n   Recall@K:")
        for k in top_k_list:
            num = avg_recall_at_k_numerator_augmented[k]
            den = avg_recall_at_k_denominator_augmented[k]
            print(f"     Recall@{k}: {avg_recall_at_k_augmented[k]:.4f} (平均召回: {num:.2f}, 平均GT: {den:.2f})")
        print("\n   Precision@K:")
        for k in top_k_list:
            num = avg_precision_at_k_numerator_augmented[k]
            den = avg_precision_at_k_denominator_augmented[k]
            print(f"     Precision@{k}: {avg_precision_at_k_augmented[k]:.4f} (平均相关: {num:.2f}, 平均检索: {den:.2f})")
        print(f"\n   F-{beta}@K:")
        for k in top_k_list:
            print(f"     F-{beta}@{k}: {avg_f_beta_augmented[k]:.4f}")
        print(f"\n   MAP: {map_augmented:.4f}")

    return evaluation_results


def main():
    """主函数：处理命令行参数"""
    parser = argparse.ArgumentParser(
        description="RAG基准测试工具：评估RAG性能",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 默认行为：运行评估
  python src/pipeline/rag_benchmark.py

  # 运行评估（自定义参数）
  python src/pipeline/rag_benchmark.py --beta 1.0

  # 使用question+evidence作为查询文本
  python src/pipeline/rag_benchmark.py --evidence

  # 使用QueryRewritter改写问题
  python src/pipeline/rag_benchmark.py --rewrite

  # 使用纯稠密检索（不使用混合检索）
  python src/pipeline/rag_benchmark.py --no-hybrid

  # 自定义top-k值
  python src/pipeline/rag_benchmark.py --top-k 1 5 10 20

  # 指定问题数据文件
  python src/pipeline/rag_benchmark.py --evidence --question src/pipeline/output/miss_tables_analysis.json

注意: 提取问题功能已移至 extract_question.py，请先运行:
  python src/pipeline/extract_question.py
        """
    )

    parser.add_argument(
        '--questions-file',
        type=str,
        help='问题数据文件路径（默认: output/question_tables_extracted.json）'
    )

    parser.add_argument(
        '--beta',
        type=float,
        default=1.0,
        help='F-β值中的β参数（默认: 1.0，即F1）'
    )
    parser.add_argument(
        '--no-hybrid',
        action='store_true',
        help='不使用混合检索（只使用稠密向量）'
    )
    parser.add_argument(
        '--top-k',
        type=int,
        nargs='+',
        default=[1, 3, 5, 10, 15, 20],
        help='要计算的Precision@K的K值列表（默认: 1 3 5 10 15 20）'
    )
    parser.add_argument(
        '--evidence',
        action='store_true',
        help='使用question+evidence作为查询文本（默认只使用question）'
    )
    parser.add_argument(
        '--rewrite',
        action='store_true',
        help='使用QueryRewritter改写question+evidence，改写后的query作为查询文本'
    )
    parser.add_argument(
        '--rag-augmented',
        action='store_true',
        help='启用RAG增强：将top-k个表在N hop内的关联表也加入到检索结果中'
    )
    parser.add_argument(
        '--hops',
        type=int,
        default=1,
        help='RAG增强时的跳数（默认: 1）'
    )
    parser.add_argument(
        '--total-limit',
        type=int,
        default=None,
        help='获取关联表时限制返回的关联表总数量（默认: 不限制）'
    )
    parser.add_argument(
        '--single-limit',
        type=int,
        default=None,
        help='获取关联表时单个源表最多返回的关联表数量（默认: 不限制）'
    )

    args = parser.parse_args()

    # 默认值
    pipeline_dir = Path(__file__).resolve().parent
    output_dir = pipeline_dir / "output"
    questions_file = Path(args.questions_file) if args.questions_file else output_dir / "question_tables_extracted.json"
    eval_output_file = output_dir / "eval_results.json"
    rewrite_output_file = output_dir / "rewrite_results.json"
    database = "bird"
    collection = "bird"

    # 检查问题数据文件是否存在
    if not questions_file.exists():
        print(f"❌ 问题数据文件不存在: {questions_file}")
        print("   请先运行提取脚本: python src/pipeline/extract_question.py")
        return

    # 异步执行评估
    eval_results = asyncio.run(evaluate_rag_performance(
        questions_file=questions_file,
        collection_name=collection,
        database=database,
        top_k_list=args.top_k,
        beta=args.beta,
        use_hybrid_search=not args.no_hybrid,
        use_evidence=args.evidence,
        use_rewrite=args.rewrite,
        rewrite_output_file=rewrite_output_file if args.rewrite else None,
        rag_augmented=args.rag_augmented,
        hops=args.hops,
        total_limit=args.total_limit,
        single_limit=args.single_limit
    ))

    # 保存评估结果
    with open(eval_output_file, 'w', encoding='utf-8') as f:
        json.dump(eval_results, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 评估结果已保存到: {eval_output_file.absolute()}")


if __name__ == "__main__":
    main()

