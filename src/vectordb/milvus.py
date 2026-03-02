import atexit
import logging
from pathlib import Path
from typing import Any, Literal

from pymilvus import AnnSearchRequest, DataType, MilvusClient, RRFRanker

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

# 支持的索引类型
IndexType = Literal["IVF_FLAT", "IVF_SQ8", "IVF_PQ", "HNSW", "AUTOINDEX", "FLAT"]

# 如果 milvus_uri 是文件路径，创建其父目录；如果是网络链接，则跳过
milvus_uri = DATAHUNT_CONFIG.MILVUS_URI
if not milvus_uri.startswith(("http://", "https://")):
    # 是文件路径，创建父目录
    Path(milvus_uri).parent.mkdir(parents=True, exist_ok=True)

_client = None

def get_milvus_client():
    """获取 Milvus 客户端单例（懒加载）"""
    global _client
    if _client is None:
        _client = MilvusClient(uri=milvus_uri, token=DATAHUNT_CONFIG.MILVUS_TOKEN)
    return _client

def _close_milvus_client():
    """关闭 Milvus 客户端（程序退出时自动调用）"""
    global _client
    if _client is not None:
        try:
            _client.close()
        except Exception:
            pass
        _client = None

atexit.register(_close_milvus_client)


class MilvusWrapper:
    """
    Milvus 向量存储封装，每个实例对应一个 collection
    """

    # 默认字段名
    FIELD_ID = "id"
    FIELD_DENSE_VECTOR = "dense_vector"
    FIELD_SPARSE_VECTOR = "sparse_vector"
    FIELD_DOCUMENT = "document"
    FIELD_METADATA = "metadata"

    def __init__(
        self,
        collection_name: str,
        dimension: int = 1024,
        max_document_length: int = 65535,
        dense_index_type: IndexType = "IVF_FLAT",
        dense_metric_type: str = "COSINE",
        sparse_metric_type: str = "IP",
        auto_create: bool = True
    ):
        """
        初始化 Milvus 向量存储，每个实例对应一个 collection

        Args:
            collection_name: collection 名称（必需）
            dimension: 稠密向量维度
            max_document_length: 文档字段最大长度
            dense_index_type: 稠密向量索引类型
                - "IVF_FLAT": 适合中等规模数据
                - "IVF_SQ8": 压缩索引，节省内存
                - "IVF_PQ": 乘积量化，高压缩比
                - "HNSW": 适合大规模数据，查询速度快
                - "FLAT": 暴力搜索，适合小规模数据
            dense_metric_type: 稠密向量距离度量，默认 COSINE（语义搜索推荐）
            auto_create: 如果 collection 不存在，是否自动创建

        注意：所有 collection 都采用稠密+稀疏向量双索引
        """
        self.collection_name = collection_name
        self.dimension = dimension
        self.max_document_length = max_document_length

        # 使用共享的客户端
        self._client = get_milvus_client()

        # 自动创建 collection（如果不存在）
        if auto_create and not self.collection_exists():
            self.create_collection(
                dense_index_type=dense_index_type,
                dense_metric_type=dense_metric_type,
                sparse_metric_type=sparse_metric_type
            )

    def collection_exists(self) -> bool:
        """检查当前 collection 是否存在"""
        return self._client.has_collection(self.collection_name)

    def create_collection(
        self,
        dense_index_type: IndexType = "IVF_FLAT",
        dense_metric_type: str = "COSINE",
        sparse_metric_type: str = "IP"
    ) -> None:
        """
        创建 collection，采用稠密+稀疏向量双索引

        Args:
            dense_index_type: 稠密向量索引类型，默认 IVF_FLAT
            dense_metric_type: 稠密向量距离度量，默认 COSINE（语义搜索推荐）
            sparse_metric_type: 稀疏向量距离度量，默认 IP
        """
        # 检查 collection 是否已存在
        if self.collection_exists():
            raise ValueError(f"Collection '{self.collection_name}' already exists")

        # 创建 schema
        schema = self._client.create_schema(
            auto_id=False,
            enable_dynamic_field=True
        )

        # 添加主键字段
        schema.add_field(
            field_name=self.FIELD_ID,
            datatype=DataType.VARCHAR,
            max_length=64,
            is_primary=True
        )

        # 添加文档字段
        schema.add_field(
            field_name=self.FIELD_DOCUMENT,
            datatype=DataType.VARCHAR,
            max_length=self.max_document_length
        )

        # 添加 metadata 字段（使用动态字段）
        # Milvus 会自动处理 JSON 字段

        # 添加稠密向量字段
        schema.add_field(
            field_name=self.FIELD_DENSE_VECTOR,
            datatype=DataType.FLOAT_VECTOR,
            dim=self.dimension
        )

        # 添加稀疏向量字段
        schema.add_field(
            field_name=self.FIELD_SPARSE_VECTOR,
            datatype=DataType.SPARSE_FLOAT_VECTOR
        )

        # 准备索引参数
        index_params = self._client.prepare_index_params()

        # 稠密向量索引
        index_params.add_index(
            field_name=self.FIELD_DENSE_VECTOR,
            index_type=dense_index_type,
            metric_type=dense_metric_type
        )

        # 稀疏向量索引
        index_params.add_index(
            field_name=self.FIELD_SPARSE_VECTOR,
            index_type="SPARSE_INVERTED_INDEX",
            metric_type=sparse_metric_type
        )

        # 创建 collection
        self._client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params
        )

    def add(
        self,
        *,
        vectors: list[list[float]],
        sparse_vectors: list[dict[int, float]] | None = None,
        documents: list[str] | None = None,
        metadatas: list[dict[str, Any]] | None = None,
        ids: list[str] | None = None
    ) -> list[str]:
        """
        添加向量数据

        Args:
            vectors: 稠密向量列表（必需）
            sparse_vectors: 稀疏向量列表，格式为 [{token_id: weight}, ...]（可选）
            documents: 文档内容列表（可选）
            metadatas: 元数据字典列表（可选），会序列化为 JSON 存储
            ids: ID 列表（可选，不提供则自动生成）

        Returns:
            插入的 ID 列表
        """
        if vectors is None or len(vectors) == 0:
            raise ValueError("vectors 参数是必需的且不能为空")

        n = len(vectors)

        # 如果提供了稀疏向量，检查长度是否一致
        if sparse_vectors is not None:
            if len(sparse_vectors) != n:
                raise ValueError("sparse_vectors 的长度必须与 vectors 一致")

        # 生成 ID
        if ids is None:
            import uuid
            ids = [str(uuid.uuid4()) for _ in range(n)]

        # 构建数据
        data = []
        for i in range(n):
            record = {
                self.FIELD_ID: ids[i],
                self.FIELD_DENSE_VECTOR: vectors[i],
                self.FIELD_DOCUMENT: "",
                self.FIELD_METADATA: {}
            }

            # 添加稀疏向量（如果提供）
            if sparse_vectors is not None:
                # 确保稀疏向量 key 是 int 类型
                sparse_dict = {int(k): float(v) for k, v in sparse_vectors[i].items()}
                record[self.FIELD_SPARSE_VECTOR] = sparse_dict
            else:
                # 如果没有提供稀疏向量，使用空字典
                record[self.FIELD_SPARSE_VECTOR] = {}

            # 添加文档
            if documents and i < len(documents):
                record[self.FIELD_DOCUMENT] = documents[i][:self.max_document_length]

            # 添加 metadata（Milvus 自动处理 dict 序列化）
            if metadatas and i < len(metadatas):
                record[self.FIELD_METADATA] = metadatas[i]

            data.append(record)

        # 插入数据
        self._client.insert(collection_name=self.collection_name, data=data)

        return ids

    def search_by_vector(
        self,
        *,
        query_vector: list[float],
        query_sparse_vector: dict[int, float] | None = None,
        top_k: int = 10,
        filter: str | None = None,
        output_fields: list[str] | None = None,
        search_params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        通过向量搜索，支持稠密检索和混合检索（稠密+稀疏）

        Args:
            query_vector: 查询稠密向量（必需）
            query_sparse_vector: 查询稀疏向量，格式为 {token_id: weight}（可选）
                如果提供，将使用混合检索；否则只使用稠密检索
            top_k: 返回结果数量
            filter: 过滤表达式
            output_fields: 返回的字段列表（默认返回 document 和 metadata）
            search_params: 搜索参数字典
                - 对于稠密检索: {"params": {"nprobe": 10}} 或 {"params": {"ef": 100}}
                - 对于混合检索: {"params": {"nprobe": 10}, "sparse_params": {"drop_ratio_search": 0.1}}
                如果不提供，将使用 Milvus 的默认搜索参数

        Returns:
            搜索结果列表，每个结果包含:
            - id: 文档 ID
            - distance/score: 向量距离或分数
            - document: 文档内容
            - metadata: 元数据字典
        """
        if not query_vector:
            raise ValueError("query_vector 参数是必需的")

        # 默认返回 document 和 metadata 字段
        if output_fields is None:
            output_fields = [self.FIELD_DOCUMENT, self.FIELD_METADATA]

        # 如果提供了稀疏向量，使用混合检索
        if query_sparse_vector is not None:
            # 确保稀疏向量 key 是 int 类型
            sparse_dict = {int(k): float(v) for k, v in query_sparse_vector.items()}

            # 创建两路检索请求
            # search_params 可以包含以下字段：
            #   - "params": 用于稠密向量检索的参数
            #     - "nprobe": 对于 IVF_* 索引类型，控制搜索的聚类中心数量（默认值由 Milvus 决定）
            #     - "ef": 对于 HNSW 索引类型，控制搜索时的候选数量（默认值由 Milvus 决定）
            #   - "sparse_params": 用于稀疏向量检索的参数（可选）
            #     - "drop_ratio_search": 搜索时丢弃的稀疏向量比例（0.0-1.0），值越大搜索越快但可能降低精度
            #   如果不提供 search_params 或相应字段，将使用 Milvus 的默认搜索参数
            hybrid_params = search_params or {}

            # 稠密检索（固定使用 COSINE 相似度）
            dense_params = hybrid_params.get("params", {})
            req_dense = AnnSearchRequest(
                data=[query_vector],
                anns_field=self.FIELD_DENSE_VECTOR,
                param={"metric_type": "COSINE", "params": dense_params},
                limit=top_k,
                expr=filter if filter else None  # 过滤条件通过 AnnSearchRequest 的 expr 参数传递
            )

            # 稀疏检索（固定使用 IP 内积）
            # 如果 search_params 中包含 sparse_params，使用它；否则使用空的 params（Milvus 默认值）
            sparse_params = hybrid_params.get("sparse_params", {})
            req_sparse = AnnSearchRequest(
                data=[sparse_dict],
                anns_field=self.FIELD_SPARSE_VECTOR,
                param={"metric_type": "IP", "params": sparse_params},
                limit=top_k,
                expr=filter if filter else None  # 过滤条件通过 AnnSearchRequest 的 expr 参数传递
            )

            # 执行混合检索
            # 使用 RRF (Reciprocal Rank Fusion) 算法融合两路检索结果
            # RRF 会自动平衡稠密向量（语义相似度）和稀疏向量（关键词匹配）的权重
            results = self._client.hybrid_search(
                collection_name=self.collection_name,
                reqs=[req_dense, req_sparse],
                ranker=RRFRanker(),
                limit=top_k,
                output_fields=output_fields
            )
        else:
            # 只使用稠密向量检索
            params = search_params or {"metric_type": "COSINE", "params": {}}
            if "metric_type" not in params:
                params["metric_type"] = "COSINE"
            results = self._client.search(
                collection_name=self.collection_name,
                data=[query_vector],
                anns_field=self.FIELD_DENSE_VECTOR,
                limit=top_k,
                filter=filter,
                output_fields=output_fields,
                search_params=params
            )

        # 格式化结果
        formatted = []
        if results and len(results) > 0:
            for hit in results[0]:
                item = {
                    "id": hit["id"],
                    "score": hit.get("score", hit.get("distance", 0.0))
                }
                # 添加其他字段（Milvus 自动返回 dict）
                entity = hit.get("entity", {})
                item.update(entity)
                formatted.append(item)

        return formatted

    def search_by_metadata(
        self,
        *,
        filter: str,
        top_k: int = 10,
        output_fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """
        通过 metadata 过滤查询（不使用向量相似度）

        Args:
            filter: 过滤表达式，例如:
                - 'metadata["source"] == "web"'
                - 'id in ["id1", "id2"]'
            top_k: 返回结果数量
            output_fields: 返回的字段列表

        Returns:
            查询结果列表，包含 id, document, metadata
        """
        if output_fields is None:
            output_fields = [self.FIELD_DOCUMENT, self.FIELD_METADATA]

        # 使用 query 接口进行标量查询（Milvus 自动返回 dict）
        return self._client.query(
            collection_name=self.collection_name,
            filter=filter,
            output_fields=output_fields,
            limit=top_k
        )

    def search_by_document(
        self,
        *,
        query_vector: list[float],
        document_filter: str | None = None,
        top_k: int = 10
    ) -> list[dict[str, Any]]:
        """
        通过文档内容搜索（结合向量相似度和文档过滤）

        注意：此方法需要先将查询文本转换为向量

        Args:
            query_vector: 查询文本的向量表示
            document_filter: 文档内容过滤（如 'document like "%关键词%"'）
            top_k: 返回结果数量

        Returns:
            搜索结果列表，包含 id, document, metadata, distance
        """
        return self.search_by_vector(
            query_vector=query_vector,
            top_k=top_k,
            filter=document_filter,
            output_fields=[self.FIELD_DOCUMENT, self.FIELD_METADATA]
        )

    def get(
        self,
        *,
        ids: list[str],
        output_fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        """
        根据 ID 获取数据

        Args:
            ids: ID 列表
            output_fields: 返回的字段列表

        Returns:
            数据列表，包含 id, document, metadata
        """
        if output_fields is None:
            output_fields = [self.FIELD_DOCUMENT, self.FIELD_METADATA]

        # Milvus 自动返回 dict
        return self._client.get(
            collection_name=self.collection_name,
            ids=ids,
            output_fields=output_fields
        )

    def delete(
        self,
        *,
        ids: list[str] | None = None,
        filter: str | None = None
    ) -> None:
        """
        删除数据

        Args:
            ids: 要删除的 ID 列表
            filter: 过滤表达式（与 ids 二选一）
        """
        if ids:
            self._client.delete(collection_name=self.collection_name, ids=ids)
        elif filter:
            self._client.delete(collection_name=self.collection_name, filter=filter)

    def count(self) -> int:
        """获取当前 collection 中的数据量"""
        stats = self._client.get_collection_stats(self.collection_name)
        return stats.get("row_count", 0)

    def get_id_by_metadata(self, key: str, value: Any) -> str | None:
        """
        根据 metadata 中的 key-value 查找记录的 ID

        Args:
            key: metadata 中的字段名（如 "table_name"）
            value: 要匹配的值

        Returns:
            匹配的记录 ID，未找到返回 None
        """
        if not self.collection_exists():
            return None

        try:
            # 使用 query 方法按 metadata 过滤，更适合此场景
            filter_expr = f'metadata["{key}"] == "{value}"'
            result = self._client.query(
                collection_name=self.collection_name,
                filter=filter_expr,
                output_fields=[self.FIELD_ID],
                limit=1
            )

            if result and len(result) > 0:
                return result[0].get(self.FIELD_ID)
            return None

        except Exception as e:
            logger.warning(f"查找 ID 失败 (key={key}, value={value}): {e}")
            return None

    def update_metadata(self, record_id: str, metadata: dict[str, Any]) -> bool:
        """
        根据记录 ID 更新 metadata

        Args:
            record_id: 记录 ID
            metadata: 要更新的 metadata 字典

        Returns:
            bool: 是否更新成功
        """
        if not self.collection_exists():
            logger.warning(f"Collection '{self.collection_name}' 不存在，无法更新 metadata")
            return False

        try:
            # upsert 时需要提供完整记录，包括原始向量和文档
            # 先查询原始记录
            result = self._client.get(
                collection_name=self.collection_name,
                ids=[record_id]
            )
            if not result:
                logger.warning(f"未找到记录 ID: {record_id}")
                return False

            original = result[0]
            # 更新 metadata，保持其他字段不变
            original[self.FIELD_METADATA] = metadata

            self._client.upsert(
                collection_name=self.collection_name,
                data=[original]
            )
            return True
        except Exception as e:
            logger.error(f"更新 metadata 失败: {e}")
            return False

    def drop_collection(self) -> None:
        """删除当前 collection"""
        if self.collection_exists():
            self._client.drop_collection(self.collection_name)
