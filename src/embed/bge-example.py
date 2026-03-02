from FlagEmbedding import BGEM3FlagModel
from pymilvus import AnnSearchRequest, DataType, MilvusClient, RRFRanker

# ============================
# 1. 初始化模型与数据库
# ============================

# 加载 BGE-M3 模型
print("正在加载 BGE-M3 模型...")
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True)

# 初始化 Milvus Lite (本地文件数据库)
client = MilvusClient("bge_m3_demo.db")

# 定义集合名称
COLLECTION_NAME = "hybrid_rag_demo"

# 如果表已存在，先删除（为了演示纯净环境）
if client.has_collection(COLLECTION_NAME):
    client.drop_collection(COLLECTION_NAME)

# ============================
# 2. 创建 Schema (关键步骤)
# ============================
# 我们需要两个向量字段：
# 1. dense_vector: 存储语义向量 (FloatVector)
# 2. sparse_vector: 存储关键词权重 (SparseFloatVector)

schema = client.create_schema(auto_id=True, enable_dynamic_field=True)

schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=1000)
# BGE-M3 默认维度 1024
schema.add_field(field_name="dense_vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
# Milvus 特有的稀疏向量类型
schema.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR)

# 定义索引参数
index_params = client.prepare_index_params()

# 稠密向量索引 (HNSW 或 IVF_FLAT)
index_params.add_index(
    field_name="dense_vector",
    index_type="IVF_FLAT",
    metric_type="COSINE",
    params={"nlist": 128}
)

# 稀疏向量索引 (必须使用 SPARSE_INVERTED_INDEX)
index_params.add_index(
    field_name="sparse_vector",
    index_type="SPARSE_INVERTED_INDEX",
    metric_type="IP", # 稀疏向量通常用内积 (Inner Product)
    params={"drop_ratio_build": 0.2}
)

# 创建集合
client.create_collection(
    collection_name=COLLECTION_NAME,
    schema=schema,
    index_params=index_params
)

print(f"集合 {COLLECTION_NAME} 创建成功。")

# ============================
# 3. 数据处理与入库 (Ingestion)
# ============================

docs = [
    "BGE-M3 是智源研究院发布的强大的多语言嵌入模型。",
    "Milvus 是一个高性能的开源向量数据库，支持混合检索。",
    "今天天气不错，适合出去野餐。",
    "机器学习中的稀疏向量可以有效捕捉精确关键词。",
]

print("正在生成向量并入库...")

# 使用 BGE-M3 生成 Dense 和 Sparse 向量
# output['dense_vecs'] 是 list of numpy arrays
# output['lexical_weights'] 是 list of dicts (这就是 Milvus 需要的稀疏格式)
output = model.encode(docs, return_dense=True, return_sparse=True)

data_to_insert = []
for i, text in enumerate(docs):
    # 注意：BGE-M3 输出的稀疏字典 key 可能是 str，Milvus 需要 int
    # 比如 {'1203': 0.4} -> {1203: 0.4}
    sparse_dict = {int(k): v for k, v in output['lexical_weights'][i].items()}

    data_to_insert.append({
        "text": text,
        "dense_vector": output['dense_vecs'][i],
        "sparse_vector": sparse_dict
    })

# 插入数据
res = client.insert(collection_name=COLLECTION_NAME, data=data_to_insert)
print(f"成功插入 {res['insert_count']} 条数据。")

# ============================
# 4. 混合检索 (Hybrid Search)
# ============================

query = "Milvus 向量数据库"

# 4.1 对 Query 生成两种向量
query_output = model.encode([query], return_dense=True, return_sparse=True)
query_dense = query_output['dense_vecs'][0]
query_sparse = {int(k): v for k, v in query_output['lexical_weights'][0].items()}

# 4.2 定义两路检索请求 (Search Requests)

# 路1：稠密检索 (语义)
search_param_dense = {
    "data": [query_dense],
    "anns_field": "dense_vector",
    "param": {"metric_type": "COSINE", "params": {"nprobe": 10}},
    "limit": 2
}
req_dense = AnnSearchRequest(**search_param_dense)

# 路2：稀疏检索 (关键词)
search_param_sparse = {
    "data": [query_sparse],
    "anns_field": "sparse_vector",
    "param": {"metric_type": "IP", "params": {"drop_ratio_search": 0.1}},
    "limit": 2
}
req_sparse = AnnSearchRequest(**search_param_sparse)

# 4.3 执行混合检索 (Hybrid Search)
# 使用 RRF (Reciprocal Rank Fusion) 倒数排名融合算法来合并两路结果
# 这是目前最推荐的无参数融合方式
results = client.hybrid_search(
    collection_name=COLLECTION_NAME,
    reqs=[req_dense, req_sparse],
    ranker=RRFRanker(), # 或者使用 WeightedRanker(0.5, 0.5)
    limit=2,
    output_fields=["text"]
)

# ============================
# 5. 输出结果
# ============================
print("\n=== 查询结果 ===")
print(f"Query: {query}")
for hit in results[0]:
    print(f"Text: {hit['entity'].get('text')}")
    print(f"Score (RRF): {hit['score']}")
    print("-" * 30)
