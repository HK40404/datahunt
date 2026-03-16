"""
SimilarSQLProvider: 通过骨架匹配获取相似 SQL

工作流程：
1. 将用户问题转换为骨架
2. 在向量数据库中搜索相似骨架
3. 返回相似问题及其 SQL
"""

import logging
from dataclasses import dataclass

from pydantic import BaseModel, Field

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from embed.bge_embedder import BGEEmbedder
from vectordb.milvus import MilvusWrapper

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class SkeletonResult(BaseModel):
    """骨架提取结果"""
    database_literals: list[str] = Field(default_factory=list, description="list of strings representing the database literals extracted from the question and evidence")
    question_skeleton: str = Field(default="", description="string representing the generated question skeleton")


@dataclass
class SimilarSQLResult:
    """相似 SQL 搜索结果"""
    question_id: int
    original_question: str
    skeleton: str
    sql: str
    score: float
    evidence: str = ""


class SimilarSQLProvider:
    """
    通过骨架匹配获取相似 SQL 的提供者

    复用 extract_question_skeleton.py 中的骨架提取逻辑，
    通过向量搜索找到相似骨架问题，返回对应的 SQL。
    """

    def __init__(
        self,
        collection_name: str = None,
        dimension: int = None,
        top_k: int = 5
    ):
        """
        初始化 SimilarSQLProvider

        Args:
            collection_name: 骨架向量数据库 collection 名称（默认从配置读取）
            dimension: 向量维度（默认从配置读取）
            top_k: 默认返回结果数量
        """
        self.collection_name = collection_name or DATAHUNT_CONFIG.SKELETON_COLLECTION
        self.dimension = dimension or 1024
        self.default_top_k = top_k

        # 初始化组件
        self._embedder = BGEEmbedder()
        self._milvus = MilvusWrapper(
            collection_name=self.collection_name,
            dimension=self.dimension,
            auto_create=False
        )

        # 检查 collection 是否存在
        self._collection_exists = self._milvus.collection_exists()
        if not self._collection_exists:
            logger.warning(f"Collection '{self.collection_name}' 不存在，SimilarSQLProvider 将跳过骨架匹配")

    async def _extract_skeleton(self, question: str) -> str:
        """
        提取问题的骨架（复用 extract_question_skeleton.py 的逻辑）

        Args:
            question: 用户问题

        Returns:
            骨架文本
        """
        from context.schema_provider import SchemaProvider
        from llm.openai import skeleton_extractor_client
        from pipeline.extract_question_skeleton import (
            QUESTION_MASK_SYSTEM,
            QUESTION_MASK_USER,
        )

        # 初始化 SchemaProvider
        schema_provider = SchemaProvider(
            collection_name="bird",
            initial_top_k=10,
            rag_hops=1,
            rag_total_limit=40
        )

        # 获取相关 schema
        matched_tables, matched_ddls = await schema_provider.schema_link(question, "bird")
        schemas_str = "\n\n".join(matched_ddls) if matched_ddls else "<empty>"

        # 构建 prompt
        user_prompt = QUESTION_MASK_USER.format(
            schemas=schemas_str,
            question=question,
            evidence="<empty>"
        )
        messages = [
            Message.system_message(QUESTION_MASK_SYSTEM),
            Message.user_message(user_prompt)
        ]

        # 使用结构化输出调用 LLM
        response = await skeleton_extractor_client.chat_structured_output(
            [m.to_dict() for m in messages],
            response_format=SkeletonResult
        )

        skeleton = response.question_skeleton.strip() if response.question_skeleton else question

        return skeleton

    def _search_similar_skeletons(
        self,
        skeleton: str,
        top_k: int
    ) -> list[dict]:
        """
        在向量数据库中搜索相似骨架

        Args:
            skeleton: 骨架文本
            top_k: 返回结果数量

        Returns:
            搜索结果列表
        """
        # 如果 collection 不存在，返回空列表
        if not self._collection_exists:
            logger.debug(f"Collection '{self.collection_name}' 不存在，跳过骨架搜索")
            return []

        # 生成稠密向量
        vectors = self._embedder.embed_texts_dense([skeleton])
        query_vector = vectors[0]

        # 执行搜索（只使用稠密向量，使用欧氏距离 L2）
        results = self._milvus.search_by_vector(
            query_vector=query_vector,
            top_k=top_k,
            output_fields=["metadata"],
            search_params={"metric_type": "L2", "params": {}}
        )

        return results

    def _parse_skeleton(self, skeleton_str: str) -> dict:
        """解析骨架 JSON 字符串"""
        import json
        try:
            return json.loads(skeleton_str)
        except json.JSONDecodeError:
            return {}

    async def find_similar_sql(
        self,
        question: str,
        top_k: int | None = None
    ) -> list[SimilarSQLResult]:
        """
        根据用户问题查找相似骨架问题及其 SQL

        Args:
            question: 用户问题
            top_k: 返回结果数量，默认使用初始化时的值

        Returns:
            相似 SQL 结果列表
        """
        if top_k is None:
            top_k = self.default_top_k

        # 1. 提取问题骨架
        try:
            skeleton = await self._extract_skeleton(question)
            logger.debug(f"问题骨架: {skeleton}")
        except Exception as e:
            logger.warning(f"骨架提取失败: {e}，跳过骨架匹配")
            return []

        # 2. 向量搜索相似骨架
        search_results = self._search_similar_skeletons(skeleton, top_k)

        # 3. 构建返回结果
        results = []
        for r in search_results:
            metadata = r.get("metadata", {})
            score = r.get("score", r.get("distance", 0.0))

            result = SimilarSQLResult(
                question_id=metadata.get("question_id", 0),
                original_question=metadata.get("original_question", ""),
                skeleton=r.get("document", ""),
                sql=metadata.get("sql", ""),
                score=score,
                evidence=metadata.get("evidence", "")
            )
            results.append(result)

        return results
