"""
Schema Provider: 提供Schema Linking功能

从向量数据库检索相关表并rerank返回top 10表
"""

import logging

from pydantic import BaseModel, Field

from config import PROJECT_LOGGER_NAME
from context.table_relation_provider import TableRelationProvider
from embed.bge_embedder import BGEEmbedder
from llm.openai import openai_client
from vectordb.milvus import MilvusWrapper

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class SkeletonResult(BaseModel):
    """骨架提取结果"""
    database_literals: list[str] = Field(default_factory=list, description="从问题中提取的数据库字面量列表")
    question_skeleton: str = Field(default="", description="生成的问题骨架")


class SchemaProvider:
    """Schema Linking提供者"""

    def __init__(
        self,
        collection_name: str = "bird",
        initial_top_k: int = 10,
        rag_hops: int = 1,
        rag_total_limit: int = 40,
        rag_single_limit: int = None
    ):
        """
        初始化SchemaProvider

        Args:
            collection_name: Milvus collection名称
            initial_top_k: 初始检索top K
            rag_hops: RAG增强跳数
            rag_total_limit: RAG增强时关联表总数限制
            rag_single_limit: RAG增强时单个表关联表数量限制，默认None（不限制）
        """
        self.collection_name = collection_name
        self.initial_top_k = initial_top_k
        self.rag_hops = rag_hops
        self.rag_total_limit = rag_total_limit
        self.rag_single_limit = rag_single_limit

        # 初始化组件
        self._embedder = BGEEmbedder()
        self._milvus = MilvusWrapper(
            collection_name=collection_name,
            dimension=1024,
            auto_create=False
        )
        self._relation_provider = TableRelationProvider()
        # 延迟导入以避免循环依赖
        from graph.reranker_llm import LLMReranker
        self._llm_reranker = LLMReranker(client=openai_client)

    def get_table_document(self, table_name: str, database: str) -> str:
        """
        根据表名从Milvus获取完整的DDL文档

        Args:
            table_name: 表名
            database: 数据库名称

        Returns:
            表的DDL文档，如果找不到返回空字符串
        """
        try:
            filter_expr = f'metadata["table_name"] == "{table_name}" and metadata["database"] == "{database}"'
            results = self._milvus.search_by_metadata(
                filter=filter_expr,
                top_k=1,
                output_fields=["document"]
            )
            if results and len(results) > 0:
                return results[0].get("document", "")
        except Exception as e:
            logger.error(f"⚠️  获取表 {table_name} 的DDL失败: {e}")
        return ""

    def get_table_metadata(self, table_name: str, database: str) -> dict:
        """
        根据表名从Milvus获取表元数据（column_types, indexes）

        Args:
            table_name: 表名
            database: 数据库名称

        Returns:
            元数据字典，包含 column_types 和 indexes，如果找不到返回空字典
        """
        try:
            filter_expr = f'metadata["table_name"] == "{table_name}" and metadata["database"] == "{database}"'
            results = self._milvus.search_by_metadata(
                filter=filter_expr,
                top_k=1,
                output_fields=["metadata"]
            )
            if results and len(results) > 0:
                metadata = results[0].get("metadata", {})
                return {
                    "column_types": metadata.get("column_types", {}),
                    "indexes": metadata.get("indexes", {})
                }
        except Exception as e:
            logger.error(f"⚠️  获取表 {table_name} 的元数据失败: {e}")
        return {"column_types": {}, "indexes": {}}

    def build_enhanced_ddl(
        self,
        document: str,
        column_types: dict[str, str],
        indexes: list[dict]
    ) -> str:
        """
        构建增强的DDL格式，包含字段类型和索引信息

        格式:
        Table: {table_name}
        Columns:
        - 字段名 (类型): 描述
        Indexes:
        - 索引名: 索引类型 (字段1, 字段2)

        Args:
            document: 原始DDL文档
            column_types: 字段类型字典 {field_name: data_type}
            indexes: 索引信息列表

        Returns:
            增强后的DDL文本
        """
        lines = []
        has_columns_section = False

        # 解析原始文档，提取表名和字段描述
        current_section = None
        field_descriptions = {}  # {field_name: description}

        for line in document.split('\n'):
            line = line.strip()
            if not line:
                continue

            if line.startswith("Table:"):
                line.replace("Table:", "").strip()
                lines.append(line)
                current_section = "table"
            elif line.startswith("Columns:"):
                # 不重复添加Columns行，直接设置current_section
                current_section = "columns"
            elif line.startswith("Example Values:"):
                # 保留 Example Values 部分
                lines.append(line)
                current_section = "example_values"
            elif line.startswith("-"):
                # 字段行
                if current_section == "columns":
                    # 确保Columns标题已添加
                    if not has_columns_section:
                        lines.append("Columns:")
                        has_columns_section = True

                    # 解析原始字段行: "- 字段名: 描述" 或 "- 字段名"
                    field_part = line[1:].strip()  # 去掉开头的 "-"
                    if ":" in field_part:
                        field_name = field_part.split(":")[0].strip()
                        description = field_part.split(":", 1)[1].strip()
                    else:
                        field_name = field_part
                        description = ""
                    field_descriptions[field_name] = description

                    # 获取字段类型
                    field_type = column_types.get(field_name, "")

                    # 构建新格式: "- 字段名 (类型): 描述"
                    if field_type:
                        if description:
                            lines.append(f"- {field_name} ({field_type}): {description}")
                        else:
                            lines.append(f"- {field_name} ({field_type})")
                    else:
                        lines.append(line)
                else:
                    # Example Values 的内容，直接保留原始格式
                    lines.append(line)
            else:
                # 处理非 "-" 开头的行（如 "Example Values:"）
                # 只有当 current_section 不是 "columns" 时才添加，避免重复添加已处理的行
                if current_section != "columns" and not line.startswith("Example Values:"):
                    lines.append(line)

        # 添加索引信息
        if indexes:
            lines.append("Indexes:")
            for idx_name, idx_info in indexes.items():
                idx_columns = idx_info.get("columns", [])
                idx_non_unique = idx_info.get("non_unique", True)

                # 根据类型生成不同的前缀
                if idx_name == "PRIMARY":
                    prefix = "PRIMARY KEY"
                elif not idx_non_unique:
                    prefix = "UNIQUE KEY"
                else:
                    prefix = "INDEX"

                # 格式化索引字段列表
                columns_str = ", ".join(idx_columns)
                if columns_str:
                    lines.append(f"- {prefix} ({columns_str})")

        return "\n".join(lines)

    def get_enhanced_document(self, table_name: str, database: str) -> str:
        """
        获取增强的DDL文档（包含字段类型和索引信息）

        Args:
            table_name: 表名
            database: 数据库名称

        Returns:
            增强后的DDL文档，如果找不到返回空字符串
        """
        # 获取原始文档
        document = self.get_table_document(table_name, database)
        if not document:
            return ""

        # 获取元数据
        metadata = self.get_table_metadata(table_name, database)

        # 构建增强DDL
        return self.build_enhanced_ddl(
            document=document,
            column_types=metadata.get("column_types", {}),
            indexes=metadata.get("indexes", {})
        )

    async def schema_link(
        self,
        query_text: str,
        database: str
    ) -> tuple[list[str], list[str]]:
        """
        Schema Linking: 从向量数据库检索相关表并rerank返回top 10表

        流程:
        1. 从向量数据库混合检索（稀疏+稠密）top 10个结果
        2. 进行1跳的RAG增强（total_limit=40）
        3. 对结果进行rerank，返回top 10表

        Args:
            query_text: 查询文本
            database: 数据库名称

        Returns:
            Tuple[匹配到的表列表, 对应的DDL列表]
        """
        logger.debug(f"数据库: {database}；查询文本: {query_text}")

        # 阶段1：从向量数据库检索
        retrieved_tables, retrieved_tables_dict = await self._retrieve_from_vector_db(query_text, database)
        logger.debug(f"阶段1-向量检索结果: {retrieved_tables}")

        # 阶段2：RAG增强
        retrieved_tables, retrieved_tables_dict = self._rag_enhance(
            retrieved_tables, retrieved_tables_dict, database
        )
        logger.debug(f"阶段2-RAG增强结果: {retrieved_tables}")

        # 阶段3：Rerank
        reranked_tables, reranked_ddls = await self._rerank(
            query_text, retrieved_tables, retrieved_tables_dict, database
        )

        # 返回结果
        if reranked_tables:
            return reranked_tables, reranked_ddls
        else:
            logger.warning("⚠️  没有找到任何表的DDL，返回原始检索结果")
            return retrieved_tables[:10] if retrieved_tables else [], []

    async def _retrieve_from_vector_db(
        self,
        query_text: str,
        database: str
    ) -> tuple[list[str], dict[str, dict]]:
        """
        第一阶段：从向量数据库检索相关表

        Args:
            query_text: 查询文本
            database: 数据库名称，用于过滤metadata

        Returns:
            Tuple[检索到的表名列表, 表名 -> {metadata, document}]
            表名列表顺序：严格按照Milvus search_results返回的顺序
        """
        retrieved_tables: list[str] = []
        retrieved_tables_dict: dict[str, dict] = {}

        # 检查collection是否存在
        if not self._milvus.collection_exists():
            logger.warning("Collection不存在，将返回空结果")
            return retrieved_tables, retrieved_tables_dict

        # 对查询文本进行embedding
        query_dense_vector = self._embedder.embed_texts_dense([query_text])[0]
        query_sparse_vector = self._embedder.embed_texts_sparse([query_text])[0]

        # 查询Milvus（混合检索，使用database作为filter_expr）
        filter_expr = f'metadata["database"] == "{database}"'
        search_results = self._milvus.search_by_vector(
            query_vector=query_dense_vector,
            query_sparse_vector=query_sparse_vector,
            top_k=self.initial_top_k,
            filter=filter_expr
        )

        # 严格按照search_results的顺序提取检索结果
        seen_tables = set()
        for res in search_results:
            metadata = res.get('metadata', {})
            document = res.get('document', '')
            table_name = metadata.get('table_name', '').lower()
            if table_name and table_name != 'unknown' and table_name not in seen_tables:
                # 按照检索结果顺序添加到列表
                retrieved_tables.append(table_name)
                retrieved_tables_dict[table_name] = {
                    'metadata': metadata,
                    'document': document
                }
                seen_tables.add(table_name)

        return retrieved_tables, retrieved_tables_dict

    def _rag_enhance(
        self,
        retrieved_tables: list[str],
        retrieved_tables_dict: dict[str, dict],
        database: str
    ) -> tuple[list[str], dict[str, dict]]:
        """
        第二阶段：RAG增强，获取关联表

        Args:
            retrieved_tables: 检索到的表名列表（阶段1的结果，保持检索顺序）
            retrieved_tables_dict: 表名 -> {metadata, document}
            database: 数据库名称

        Returns:
            Tuple[增强后的表名列表, 更新后的表名->DDL映射]
            表名列表顺序：先阶段1的表（保持检索顺序），再阶段2的关联表（保持get_connected_tables返回顺序）
        """

        # 使用有序集合记录已添加的表，确保顺序
        seen_tables = set(retrieved_tables)
        enhanced_tables = list(retrieved_tables)  # 复制阶段1的结果，保持顺序

        try:
            # 获取在关系图中存在的表
            tables_in_graph = [t for t in retrieved_tables if self._relation_provider.has_table(t)]

            if tables_in_graph:
                related_tables = self._relation_provider.get_connected_tables(
                    tables_in_graph,
                    max_hops=self.rag_hops,
                    total_limit=self.rag_total_limit,
                    single_limit=self.rag_single_limit
                )

                # 按照get_connected_tables返回的顺序，逐个添加关联表
                for related_table in related_tables:
                    # 只添加未在阶段1出现过的表
                    if related_table not in seen_tables:
                        # 获取关联表的metadata和document
                        document = self.get_table_document(related_table, database)
                        retrieved_tables_dict[related_table] = {
                            'metadata': {'table_name': related_table},
                            'document': document
                        }
                        # 严格按照顺序添加到列表末尾
                        enhanced_tables.append(related_table)
                        seen_tables.add(related_table)
        except Exception as e:
            logger.warning(f"RAG增强失败: {e}")

        return enhanced_tables, retrieved_tables_dict

    async def _rerank(
        self,
        query_text: str,
        retrieved_tables: list[str],
        retrieved_tables_dict: dict[str, dict],
        database: str
    ) -> tuple[list[str], list[str]]:
        """
        第三阶段：使用LLM进行Rerank

        Args:
            query_text: 查询文本
            retrieved_tables: 检索到的表名列表（阶段1+阶段2的结果，保持顺序）
            retrieved_tables_dict: 表名 -> {metadata, document}
            database: 数据库名称

        Returns:
            Tuple[重排序后的表名列表, 对应的DDL列表]
            表名列表顺序：严格按照LLM rerank返回的顺序
        """

        # 构建表描述文本（使用增强DDL格式，包含字段类型和索引信息）
        table_schemas: list[str] = []
        table_names: list[str] = []
        for table_name in retrieved_tables:
            # 使用增强DDL格式
            enhanced_doc = self.get_enhanced_document(table_name, database)
            if enhanced_doc:
                table_schemas.append(enhanced_doc)
                table_names.append(table_name)

        if not table_schemas:
            logger.warning("没有找到任何表的DDL")
            return [], []

        # 构建schema字典
        table_schemas_dict: dict[str, str] = {}
        for table_name, document in zip(table_names, table_schemas):
            table_schemas_dict[table_name] = document

        # 调用LLM rerank（后处理：去重+有效性检查+数量调整 已在LLMReranker中完成）
        rerank_result = await self._llm_reranker.rerank(
            query=query_text,
            schemas=table_schemas_dict
        )

        # 直接使用 rerank_result.schema_list 构建结果
        schema_list = rerank_result.schema_list

        # 构建结果
        reranked_tables = [table_names[idx] for idx in schema_list]
        reranked_ddls = [table_schemas[idx] for idx in schema_list]

        # 一行打印Top 10表
        tables_str = ", ".join(reranked_tables)
        logger.debug(f"Rerank后Top 10表: {tables_str}")

        return reranked_tables, reranked_ddls
