#!/usr/bin/env python3
"""
提取问题骨架并存储到向量数据库

从 dev.json 读取问题，调用 LLM 提取语义骨架，
将骨架文本和 SQL 存储到向量数据库。
"""

import argparse
import asyncio
import json
import logging
import time

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from embed.bge_embedder import BGEEmbedder
from llm.openai import skeleton_extractor_client
from vectordb.metadata import QuestionMetadata
from vectordb.milvus import MilvusWrapper

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

# 路径配置
DEV_JSON = "data/dev_20240627/dev.json"
EXCLUDE_JSON = "src/pipeline/data/mini_dev_mysql.json"
COLLECTION_NAME = DATAHUNT_CONFIG.SKELETON_COLLECTION

# 从配置加载 question_mask prompt
PROMPT_CONFIG = DATAHUNT_CONFIG.PROMPT.question_mask
QUESTION_MASK_SYSTEM = PROMPT_CONFIG.system
QUESTION_MASK_USER = PROMPT_CONFIG.user


def load_and_filter_questions(dev_path: str, exclude_path: str) -> list[dict]:
    """加载 dev.json，排除已存在的问题"""
    with open(dev_path, encoding='utf-8') as f:
        dev_data = json.load(f)

    with open(exclude_path, encoding='utf-8') as f:
        exclude_data = json.load(f)
    exclude_ids = {q['question_id'] for q in exclude_data}

    filtered = [q for q in dev_data if q['question_id'] not in exclude_ids]
    logger.info(f"加载 {len(dev_data)} 个问题，排除 {len(exclude_ids)} 个，剩余 {len(filtered)} 个")
    return filtered


async def extract_single_skeleton(
    schema_provider,
    question: str,
    evidence: str,
    question_id: int
) -> str:
    """
    提取单个问题的骨架

    Args:
        schema_provider: SchemaProvider 实例
        question: 用户问题
        evidence: 证据
        question_id: 问题 ID（用于日志）

    Returns:
        骨架文本
    """
    # 使用 SchemaProvider.schema_link 获取 top 10 相关表
    matched_tables, matched_ddls = await schema_provider.schema_link(question, "bird")

    # 拼接 schema（参考 sql_generator._build_user_prompt）
    schemas_str = "\n\n".join(matched_ddls) if matched_ddls else "<empty>"

    # 构建用户 prompt
    user_prompt = QUESTION_MASK_USER.format(
        schemas=schemas_str,
        question=question,
        evidence=evidence if evidence else "<empty>"
    )
    messages = [
        Message.system_message(QUESTION_MASK_SYSTEM),
        Message.user_message(user_prompt)
    ]

    # 延迟导入以避免循环依赖
    from context.schema_provider import SkeletonResult

    # 使用结构化输出调用 LLM
    response = await skeleton_extractor_client.chat_structured_output(
        [m.to_dict() for m in messages],
        response_format=SkeletonResult
    )

    # 提取骨架文本
    skeleton = response.question_skeleton.strip() if response.question_skeleton else question

    return skeleton


async def extract_skeletons(
    questions: list[dict],
    concurrency: int = 5
) -> list[str]:
    """
    调用 LLM 提取每个问题的骨架（使用 question_mask prompt + schema 召回）

    Args:
        questions: 问题列表
        concurrency: 并发度，默认5

    Returns:
        骨架列表
    """
    # 延迟导入以避免循环依赖
    from context.schema_provider import SchemaProvider

    # 初始化 SchemaProvider（复用已有的 RAG 增强和 rerank 逻辑）
    schema_provider = SchemaProvider(
        collection_name="bird",
        initial_top_k=10,
        rag_hops=1,
        rag_total_limit=40
    )

    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(concurrency)

    # 进度跟踪
    progress_state = {'completed': 0, 'total': len(questions)}
    progress_lock = asyncio.Lock()
    start_time = time.time()

    async def process_item(item: dict):
        async with semaphore:
            question = item['question']
            evidence = item.get('evidence', '')
            question_id = item.get('question_id', '?')

            skeleton = await extract_single_skeleton(
                schema_provider, question, evidence, question_id
            )

            # 更新进度
            async with progress_lock:
                progress_state['completed'] += 1
                completed = progress_state['completed']
                total = progress_state['total']
                progress_pct = (completed / total) * 100
                elapsed = time.time() - start_time
                # ETA = 预估总时间 - 已用时间 = (elapsed / completed * total) - elapsed
                # 简化: eta = elapsed * (total - completed) / completed
                eta = (elapsed * (total - completed) / completed) if completed > 0 else 0
                bar_length = 30
                filled_length = int(bar_length * completed // total)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)

                logger.info(
                    f"[{bar}] {progress_pct:5.1f}% | "
                    f"[{completed:3d}/{total}] ID:{question_id:4d} | "
                    f"ETA: {eta:.0f}秒"
                )

            return skeleton

    logger.info(f"开始提取骨架 (并发度: {concurrency})...")

    # 并发执行
    tasks = [process_item(q) for q in questions]
    skeletons = await asyncio.gather(*tasks)

    logger.info(f"完成骨架提取，共 {len(skeletons)} 个")
    return skeletons


def save_to_vector_db(
    skeletons: list[str],
    questions: list[dict],
    collection_name: str
) -> None:
    """将骨架和 SQL 保存到向量数据库（只用稠密向量）"""
    # 生成稠密向量
    embedder = BGEEmbedder()
    logger.info("生成稠密向量...")
    vectors = embedder.embed_texts_dense(skeletons)

    # 准备数据，使用 QuestionMetadata 结构化
    documents = skeletons
    metadatas = []
    for q, skeleton in zip(questions, skeletons):
        meta = QuestionMetadata(
            question_id=q['question_id'],
            db_id='bird',
            type='question_skeleton',
            original_question=q['question'],
            evidence=q.get('evidence', ''),
            sql=q['SQL'],
            database_literals=extract_database_literals(skeleton)
        )
        metadatas.append(meta.__dict__)
    ids = [str(q['question_id']) for q in questions]

    # 保存到向量数据库（只用稠密向量）
    milvus = MilvusWrapper(collection_name=collection_name, dimension=1024, dense_metric_type="L2", auto_create=True)
    milvus.add(
        vectors=vectors,
        sparse_vectors=None,  # 不用稀疏向量
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

    logger.info(f"已保存 {len(skeletons)} 条记录到 collection '{collection_name}'")


def parse_skeleton(skeleton: str) -> dict:
    """解析骨架 JSON 字符串，返回字典"""
    try:
        return json.loads(skeleton)
    except json.JSONDecodeError:
        return {}


def extract_database_literals(skeleton: str) -> list[str]:
    """从骨架中提取 database_literals 列表"""
    parsed = parse_skeleton(skeleton)
    return parsed.get("database_literals", [])


def compare_and_display(skeletons: list[str], questions: list[dict]) -> None:
    """比较骨架与原问题，展示差异"""
    logger.info("\n" + "=" * 80)
    logger.info("骨架与原问题对比")
    logger.info("=" * 80)

    for i, (q, skeleton) in enumerate(zip(questions, skeletons)):
        logger.info(f"\n[{i+1}] 问题ID: {q['question_id']}")
        logger.info(f"原问题: {q['question']}")
        logger.info(f"骨架: {skeleton}")
        logger.info("-" * 40)

    logger.info("\n" + "=" * 80)
    logger.info(f"共处理 {len(skeletons)} 个问题")
    logger.info("=" * 80)


async def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='提取问题骨架并处理')
    parser.add_argument('--input', type=str, default=None, help='输入的JSON文件路径')
    parser.add_argument('--limit', type=int, default=None, help='限制处理的问题数量')
    parser.add_argument('--not-store', action='store_true', help='不保存到数据库，仅比较并展示骨架与原问题')
    parser.add_argument('--concurrency', type=int, default=20, help='并发度，默认20')
    parser.add_argument('--clear', action='store_true', help='运行前清空对应的 collection')
    args = parser.parse_args()

    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 1. 加载并过滤数据
    input_path = args.input if args.input else DEV_JSON
    logger.info(f"使用输入文件: {input_path}")
    questions = load_and_filter_questions(input_path, EXCLUDE_JSON)

    # 应用 limit 限制
    if args.limit:
        questions = questions[:args.limit]
        logger.info(f"限制处理前 {args.limit} 个问题")

    # 2. 如果指定 --clear，先清空 collection
    if args.clear and not args.not_store:
        logger.info(f"清空 collection '{COLLECTION_NAME}'...")
        milvus = MilvusWrapper(collection_name=COLLECTION_NAME, dimension=1024, dense_metric_type="L2", auto_create=False)
        if milvus.collection_exists():
            milvus.drop_collection()
            logger.info(f"已清空 collection '{COLLECTION_NAME}'")

    # 3. 提取骨架（支持并发）
    skeletons = await extract_skeletons(questions, concurrency=args.concurrency)
    # 4. 根据选项处理结果
    if args.not_store:
        # 仅比较并展示
        compare_and_display(skeletons, questions)
    else:
        # 保存到向量数据库
        save_to_vector_db(skeletons, questions, COLLECTION_NAME)

    logger.info("完成！")


if __name__ == "__main__":
    asyncio.run(main())
