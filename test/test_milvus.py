import os
import time
import uuid

import pytest

from vectordb.milvus import MilvusWrapper


@pytest.fixture(scope="function")
def test_collection():
    """为每个测试创建独立的 collection"""
    collection_name = f"test_collection_{uuid.uuid4().hex[:8]}"
    return collection_name


@pytest.fixture(scope="function")
def store(test_collection):
    """创建测试用的 MilvusWrapper 实例，测试后清理"""
    store = MilvusWrapper(
        collection_name=test_collection,
        dimension=128,  # 使用较小维度加快测试
        dense_index_type="FLAT",  # 使用 FLAT 索引加快测试
        auto_create=True
    )
    yield store
    # 清理：删除测试 collection
    if store.collection_exists():
        store.drop_collection()

def test_manual():
    milvus = MilvusWrapper(
        collection_name="bird",
        dimension=1024,
        auto_create=False
    )
    print("******* *******")
    # 查表
    # table_name = "customers"
    # table_filter_results = milvus.search_by_metadata(
    #     filter=f'metadata["table_name"] == "{table_name}"',
    #     top_k=1
    # )
    # print(table_filter_results[0]["document"])
    
    # 查向量（稠密+稀疏）
    query = "What is the overall rating of the football player Gabriel Tamas in year 2011?"
    from embed.bge_embedder import BGEEmbedder
    embedder = BGEEmbedder()
    hybrid_vec = embedder.embed_texts_hybrid([query])[0]
    results = milvus.search_by_vector(
        query_vector=hybrid_vec.dense_embedding,
        query_sparse_vector=hybrid_vec.sparse_embedding,
        top_k=10
    )
    for result in results:
        print(result.get("metadata", {}).get("table_name", ""))
    print("******* *******")

    

def test_initialization_auto_create(test_collection):
    """测试初始化时自动创建 collection"""
    store = MilvusWrapper(
        collection_name=test_collection,
        dimension=128,
        auto_create=True
    )
    assert store.collection_exists()
    store.drop_collection()


def test_initialization_no_auto_create(test_collection):
    """测试初始化时不自动创建 collection"""
    store = MilvusWrapper(
        collection_name=test_collection,
        dimension=128,
        auto_create=False
    )
    assert not store.collection_exists()
    # 手动创建
    store.create_collection()
    assert store.collection_exists()
    store.drop_collection()


def test_create_collection(store):
    """测试手动创建 collection"""
    # store fixture 已经创建了 collection，先删除
    store.drop_collection()
    assert not store.collection_exists()
    
    # 重新创建
    store.create_collection()
    assert store.collection_exists()


def test_create_collection_already_exists(store):
    """测试创建已存在的 collection 会抛出错误"""
    with pytest.raises(ValueError, match="already exists"):
        store.create_collection()


def test_add_dense_only(store):
    """测试只添加稠密向量"""
    vectors = [[0.1] * 128, [0.2] * 128, [0.3] * 128]
    documents = ["文档1", "文档2", "文档3"]
    
    start_time = time.time()
    ids = store.add(vectors=vectors, documents=documents)
    end_time = time.time()
    
    assert len(ids) == 3
    assert all(isinstance(id, str) for id in ids)
    assert store.count() == 3
    print(f"\n[Time] 添加3条数据耗时: {end_time - start_time:.4f}s")


def test_add_dense_with_sparse(store):
    """测试添加稠密+稀疏向量"""
    vectors = [[0.1] * 128, [0.2] * 128]
    sparse_vectors = [{1203: 0.4, 4567: 0.8}, {2345: 0.6, 5678: 0.9}]
    documents = ["文档1", "文档2"]
    
    start_time = time.time()
    ids = store.add(
        vectors=vectors,
        sparse_vectors=sparse_vectors,
        documents=documents
    )
    end_time = time.time()
    
    assert len(ids) == 2
    assert store.count() == 2
    print(f"\n[Time] 添加2条数据（稠密+稀疏）耗时: {end_time - start_time:.4f}s")


def test_add_with_metadata(store):
    """测试添加带 metadata 的数据"""
    vectors = [[0.1] * 128]
    metadatas = [{"source": "web", "author": "test"}]
    
    ids = store.add(vectors=vectors, metadatas=metadatas)
    
    assert len(ids) == 1
    # 验证 metadata 是否正确存储
    results = store.get(ids=ids)
    assert len(results) == 1
    assert results[0]["metadata"]["source"] == "web"
    assert results[0]["metadata"]["author"] == "test"


def test_add_with_custom_ids(store):
    """测试使用自定义 ID"""
    vectors = [[0.1] * 128]
    custom_ids = ["custom_id_1"]
    
    ids = store.add(vectors=vectors, ids=custom_ids)
    
    assert ids == custom_ids
    results = store.get(ids=custom_ids)
    assert len(results) == 1
    assert results[0]["id"] == "custom_id_1"


def test_add_empty_vectors(store):
    """测试添加空向量列表会抛出错误"""
    with pytest.raises(ValueError, match="必需的且不能为空"):
        store.add(vectors=[])


def test_add_mismatched_lengths(store):
    """测试向量长度不匹配会抛出错误"""
    vectors = [[0.1] * 128, [0.2] * 128]
    sparse_vectors = [{1203: 0.4}]  # 长度不匹配
    
    with pytest.raises(ValueError, match="sparse_vectors 的长度必须与 vectors 一致"):
        store.add(vectors=vectors, sparse_vectors=sparse_vectors)


def test_search_dense_only(store):
    """测试只使用稠密向量搜索"""
    # 添加测试数据
    vectors = [[0.1] * 128, [0.2] * 128, [0.3] * 128]
    documents = ["文档1", "文档2", "文档3"]
    store.add(vectors=vectors, documents=documents)
    
    # 搜索
    query_vector = [0.15] * 128  # 接近第一个向量
    start_time = time.time()
    results = store.search_by_vector(query_vector=query_vector, top_k=2)
    end_time = time.time()
    
    assert len(results) == 2
    assert "id" in results[0]
    assert "score" in results[0] or "distance" in results[0]
    assert "document" in results[0]
    print(f"\n[Time] 稠密向量搜索耗时: {end_time - start_time:.4f}s")


def test_search_hybrid(store):
    """测试混合搜索（稠密+稀疏）"""
    # 添加测试数据
    vectors = [[0.1] * 128, [0.2] * 128]
    sparse_vectors = [{1203: 0.4, 4567: 0.8}, {2345: 0.6}]
    documents = ["文档1", "文档2"]
    store.add(vectors=vectors, sparse_vectors=sparse_vectors, documents=documents)
    
    # 混合搜索
    query_vector = [0.15] * 128
    query_sparse_vector = {1203: 0.5, 4567: 0.7}
    start_time = time.time()
    results = store.search_by_vector(
        query_vector=query_vector,
        query_sparse_vector=query_sparse_vector,
        top_k=2
    )
    end_time = time.time()
    
    assert len(results) == 2
    assert "id" in results[0]
    assert "score" in results[0]
    print(f"\n[Time] 混合搜索耗时: {end_time - start_time:.4f}s")


def test_search_with_params(store):
    """测试带搜索参数的搜索"""
    vectors = [[0.1] * 128, [0.2] * 128]
    store.add(vectors=vectors)
    
    query_vector = [0.15] * 128
    search_params = {"params": {"nprobe": 10}}
    
    results = store.search_by_vector(
        query_vector=query_vector,
        search_params=search_params,
        top_k=2
    )
    
    assert len(results) == 2


def test_search_hybrid_with_params(store):
    """测试混合搜索带参数"""
    vectors = [[0.1] * 128]
    sparse_vectors = [{1203: 0.4}]
    store.add(vectors=vectors, sparse_vectors=sparse_vectors)
    
    query_vector = [0.15] * 128
    query_sparse_vector = {1203: 0.5}
    search_params = {
        "params": {"nprobe": 10},
        "sparse_params": {"drop_ratio_search": 0.1}
    }
    
    results = store.search_by_vector(
        query_vector=query_vector,
        query_sparse_vector=query_sparse_vector,
        search_params=search_params,
        top_k=1
    )
    
    assert len(results) == 1


def test_search_empty_query_vector(store):
    """测试空查询向量会抛出错误"""
    with pytest.raises(ValueError, match="query_vector 参数是必需的"):
        store.search_by_vector(query_vector=[])


def test_search_by_metadata(store):
    """测试通过 metadata 搜索"""
    vectors = [[0.1] * 128, [0.2] * 128]
    metadatas = [{"source": "web"}, {"source": "file"}]
    store.add(vectors=vectors, metadatas=metadatas)
    
    results = store.search_by_metadata(
        filter='metadata["source"] == "web"',
        top_k=10
    )
    
    assert len(results) == 1
    assert results[0]["metadata"]["source"] == "web"


def test_search_by_document(store):
    """测试通过文档内容搜索"""
    vectors = [[0.1] * 128, [0.2] * 128]
    documents = ["人工智能", "机器学习"]
    store.add(vectors=vectors, documents=documents)
    
    query_vector = [0.15] * 128
    results = store.search_by_document(
        query_vector=query_vector,
        document_filter='document like "%人工智能%"',
        top_k=10
    )
    
    assert len(results) >= 1


def test_get(store):
    """测试根据 ID 获取数据"""
    vectors = [[0.1] * 128]
    documents = ["测试文档"]
    ids = store.add(vectors=vectors, documents=documents)
    
    results = store.get(ids=ids)
    
    assert len(results) == 1
    assert results[0]["id"] == ids[0]
    assert results[0]["document"] == "测试文档"


def test_delete_by_ids(store):
    """测试通过 ID 删除数据"""
    vectors = [[0.1] * 128, [0.2] * 128]
    ids = store.add(vectors=vectors)
    
    assert store.count() == 2
    
    store.delete(ids=[ids[0]])
    
    assert store.count() == 1
    remaining = store.get(ids=[ids[1]])
    assert len(remaining) == 1
    assert remaining[0]["id"] == ids[1]


def test_delete_by_filter(store):
    """测试通过 filter 删除数据"""
    vectors = [[0.1] * 128, [0.2] * 128]
    metadatas = [{"source": "web"}, {"source": "file"}]
    ids = store.add(vectors=vectors, metadatas=metadatas)
    
    assert store.count() == 2
    
    store.delete(filter='metadata["source"] == "web"')
    
    assert store.count() == 1
    remaining = store.get(ids=[ids[1]])
    assert remaining[0]["metadata"]["source"] == "file"


def test_count(store):
    """测试获取数据量"""
    assert store.count() == 0
    
    vectors = [[0.1] * 128, [0.2] * 128, [0.3] * 128]
    store.add(vectors=vectors)
    
    assert store.count() == 3


def test_drop_collection(store):
    """测试删除 collection"""
    assert store.collection_exists()
    
    store.drop_collection()
    
    assert not store.collection_exists()


def test_collection_exists(store):
    """测试检查 collection 是否存在"""
    assert store.collection_exists()
    
    store.drop_collection()
    
    assert not store.collection_exists()


def test_multiple_collections():
    """测试多个 collection 可以独立工作"""
    collection1 = f"test_collection_1_{uuid.uuid4().hex[:8]}"
    collection2 = f"test_collection_2_{uuid.uuid4().hex[:8]}"
    
    store1 = MilvusWrapper(collection_name=collection1, dimension=128, auto_create=True)
    store2 = MilvusWrapper(collection_name=collection2, dimension=128, auto_create=True)
    
    # 向两个 collection 添加不同的数据
    store1.add(vectors=[[0.1] * 128], documents=["collection1"])
    store2.add(vectors=[[0.2] * 128], documents=["collection2"])
    
    assert store1.count() == 1
    assert store2.count() == 1
    
    # 清理
    store1.drop_collection()
    store2.drop_collection()


@pytest.mark.manual
def test_ddl_embed_data_in_milvus():
    """
    测试 ddl_embed.py 执行后，数据是否成功写入向量数据库
    
    这是一个集成测试，用于验证执行完 ddl_embed.py 后，Milvus 中是否正确写入了数据库 DDL。
    默认不执行，需要手动指定才执行。
    
    使用方法：
        TEST_DDL_EMBED=1 pytest test/test_milvus.py::test_ddl_embed_data_in_milvus -v
    """
    # 检查是否设置了环境变量来启用此测试
    if not os.getenv("TEST_DDL_EMBED"):
        pytest.skip("此测试需要手动执行。设置环境变量 TEST_DDL_EMBED=1 来运行此测试")
    
    # 使用 ddl_embed.py 中默认的 collection 名称和数据库名称
    collection_name = "bird"
    database_name = "bird"
    
    # 连接到 Milvus，检查已存在的 collection
    milvus = MilvusWrapper(
        collection_name=collection_name,
        dimension=1024,  # BGE-M3 的维度
        auto_create=False
    )
    
    # 验证 collection 存在
    assert milvus.collection_exists(), f"Collection '{collection_name}' 应该存在，请先执行 ddl_embed.py"
    
    # 验证数据量（应该大于 0）
    count = milvus.count()
    assert count > 0, f"Collection '{collection_name}' 中应该有数据，实际有 {count} 条"
    print(f"\n✅ Collection '{collection_name}' 中存在 {count} 条数据")
    
    # 验证可以通过 metadata 搜索到数据
    results = milvus.search_by_metadata(
        filter=f'metadata["database"] == "{database_name}"',
        top_k=100  # 获取更多数据用于验证
    )
    assert len(results) > 0, f"应该能找到 database='{database_name}' 的数据"
    print(f"✅ 找到 {len(results)} 条 database='{database_name}' 的数据")
    
    # 验证 metadata 结构正确
    for result in results[:10]:  # 只检查前10条，避免输出过多
        assert "metadata" in result, "结果应该包含 metadata"
        assert result["metadata"]["type"] == "database_schema", \
            f"metadata.type 应该是 'database_schema'，实际是 '{result['metadata'].get('type')}'"
        assert result["metadata"]["database"] == database_name, \
            f"metadata.database 应该是 '{database_name}'，实际是 '{result['metadata'].get('database')}'"
        assert "table_name" in result["metadata"], "metadata 应该包含 table_name"
        assert result["metadata"]["table_name"] != "unknown", \
            f"table_name 不应该是 'unknown'，实际是 '{result['metadata']['table_name']}'"
    
    print("✅ Metadata 结构验证通过")
    
    # 验证可以通过文档内容搜索到数据
    # 使用 BGE embedder 生成查询向量
    from embed.bge_embedder import BGEEmbedder
    embedder = BGEEmbedder()
    
    # 搜索包含表结构相关的查询
    query_text = "table schema CREATE TABLE"
    query_vector = embedder.embed_texts_dense([query_text])[0]
    
    search_results = milvus.search_by_vector(
        query_vector=query_vector,
        top_k=5
    )
    
    assert len(search_results) > 0, "应该能找到相关的表结构数据"
    print(f"✅ 向量搜索找到 {len(search_results)} 条相关数据")
    
    # 验证搜索结果包含 document 字段
    for result in search_results:
        assert "document" in result, "搜索结果应该包含 document 字段"
        assert "Table:" in result["document"], "document 应该包含 'Table:' 前缀"
        assert "CREATE TABLE" in result["document"], "document 应该包含 'CREATE TABLE'"
    
    print("✅ 搜索结果格式验证通过")
    
    # 验证可以通过 table_name 过滤搜索（随机选择一个表名）
    sample_table_name = results[0]["metadata"]["table_name"]
    table_filter_results = milvus.search_by_metadata(
        filter=f'metadata["table_name"] == "{sample_table_name}"',
        top_k=1
    )
    assert len(table_filter_results) == 1, f"应该能找到 table_name='{sample_table_name}' 的表"
    assert table_filter_results[0]["metadata"]["table_name"] == sample_table_name
    print(f"✅ 通过 table_name='{sample_table_name}' 过滤搜索成功")
    
    # 验证混合搜索（稠密+稀疏向量）
    query_sparse_vector = embedder.embed_texts_sparse([query_text])[0]
    hybrid_results = milvus.search_by_vector(
        query_vector=query_vector,
        query_sparse_vector=query_sparse_vector,
        top_k=5
    )
    assert len(hybrid_results) > 0, "混合搜索应该能找到相关数据"
    print(f"✅ 混合搜索找到 {len(hybrid_results)} 条相关数据")
    
    print(f"\n✅ 所有验证通过！Collection '{collection_name}' 中的数据已正确写入。")

