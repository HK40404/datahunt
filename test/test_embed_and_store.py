import uuid

import pytest

from embed.bge_embedder import BGEEmbedder
from vectordb.milvus import MilvusWrapper


@pytest.fixture(scope="module")
def embedder():
    """创建一个共享的 embedder 实例"""
    return BGEEmbedder()


@pytest.fixture(scope="function")
def test_collection():
    """为每个测试创建独立的 collection 名称"""
    return f"test_bird_{uuid.uuid4().hex[:8]}"


@pytest.fixture(scope="function")
def milvus_store(test_collection):
    """创建测试用的 MilvusWrapper 实例，测试后清理"""
    store = MilvusWrapper(
        collection_name=test_collection,
        dimension=1024,  # BGE-M3 稠密向量维度
        auto_create=True
    )
    yield store
    # 清理：删除测试 collection
    if store.collection_exists():
        store.drop_collection()


def test_embed_and_store(embedder, milvus_store, test_collection):
    """
    测试embedding和存储功能
    使用模拟的DDL数据进行测试，真实存储到数据库，然后检索验证，最后删除测试数据
    """
    print("=" * 60)
    print("开始测试 embedding 和存储功能")
    print("=" * 60)
    
    # 创建测试用的DDL数据
    test_ddls = [
        """Table: users
CREATE TABLE users (
    id INT PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(100) -- 样本: ["user1@example.com", "user2@example.com"]
);
""",
        """Table: orders
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT,
    total_amount DECIMAL(10, 2) -- 样本: [100.50, 200.75, 300.00],
    status VARCHAR(20) -- 样本: ["pending", "completed", "cancelled"]
);
""",
        """Table: products
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    name VARCHAR(200) -- 样本: ["Product A", "Product B"],
    price DECIMAL(10, 2),
    category VARCHAR(50) -- 样本: ["Electronics", "Clothing"]
);
"""
    ]
    
    database = "test_db"
    stored_ids = []  # 保存存储的ID，用于后续删除
    
    print(f"\n准备测试数据：{len(test_ddls)} 个DDL")
    
    try:
        # 1. 存储测试数据
        print("\n步骤1: 存储测试数据到Milvus...")
        dense_vectors = embedder.embed_texts_dense(test_ddls)
        sparse_vectors = embedder.embed_texts_sparse(test_ddls)
        
        # 生成ID和metadata
        ids = []
        metadatas = []
        for i, ddl_text in enumerate(test_ddls):
            table_name = "unknown"
            if ddl_text.startswith("Table: "):
                table_name = ddl_text.split("\n")[0].replace("Table: ", "").strip()
            
            ids.append(str(uuid.uuid4()))
            metadatas.append({
                "type": "database_schema",
                "database": database,
                "table_name": table_name
            })
        
        stored_ids = ids  # 保存ID用于后续删除
        
        # 存储到Milvus
        milvus_store.add(
            vectors=dense_vectors,
            sparse_vectors=sparse_vectors,
            documents=test_ddls,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ 已存储 {len(test_ddls)} 个DDL到Milvus")
        
        # 2. 验证存储的数据量
        count = milvus_store.count()
        print(f"\n步骤2: 验证存储的数据量 - 当前collection中有 {count} 条数据")
        assert count >= len(test_ddls), f"存储的数据量不正确：期望至少 {len(test_ddls)} 条，实际 {count} 条"
        
        # 3. 检索测试：使用第一个DDL的向量进行检索
        print("\n步骤3: 进行检索测试...")
        query_text = test_ddls[0]  # 使用第一个DDL作为查询
        query_dense = embedder.embed_texts_dense([query_text])[0]
        query_sparse = embedder.embed_texts_sparse([query_text])[0]
        
        # 使用混合检索（稠密+稀疏）
        results = milvus_store.search_by_vector(
            query_vector=query_dense,
            query_sparse_vector=query_sparse,
            top_k=3
        )
        
        print(f"✅ 检索到 {len(results)} 条结果")
        assert len(results) > 0, "检索结果为空"
        
        # 验证检索结果
        print("\n步骤4: 验证检索结果...")
        found_original = False
        for i, result in enumerate(results):
            print(f"  结果 {i+1}: ID={result.get('id')}, Score={result.get('score', 0):.4f}")
            print(f"    表名: {result.get('metadata', {}).get('table_name', 'unknown')}")
            if result.get('id') in stored_ids:
                found_original = True
                print("    ✅ 找到原始存储的数据")
        
        assert found_original, "检索结果中没有找到原始存储的数据"
        
        # 4. 测试metadata过滤
        print("\n步骤5: 测试metadata过滤...")
        filter_results = milvus_store.search_by_vector(
            query_vector=query_dense,
            query_sparse_vector=query_sparse,
            top_k=10,
            filter='metadata["table_name"] == "users"'
        )
        print(f"✅ 使用metadata过滤后找到 {len(filter_results)} 条结果")
        if filter_results:
            assert filter_results[0].get('metadata', {}).get('table_name') == 'users', "过滤结果不正确"
        
        # 5. 清理测试数据
        print("\n步骤6: 清理测试数据...")
        milvus_store.delete(ids=stored_ids)
        count_after_delete = milvus_store.count()
        print(f"✅ 已删除测试数据，当前collection中有 {count_after_delete} 条数据")
        assert count_after_delete < count, "删除数据后数量未减少"
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过：embedding和存储功能正常")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        
        # 确保清理测试数据
        try:
            if stored_ids:
                print("\n清理测试数据...")
                if milvus_store.collection_exists():
                    milvus_store.delete(ids=stored_ids)
                    print("✅ 已清理测试数据")
        except Exception as cleanup_error:
            print(f"⚠️  清理测试数据时出错：{cleanup_error}")
        
        # 重新抛出异常以便 pytest 捕获
        raise
