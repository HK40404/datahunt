import time

import pytest

from embed.base_embedder import EmbedResult
from embed.bge_embedder import BGEEmbedder


@pytest.fixture(scope="module")
def embedder():
    """创建一个共享的 embedder 实例，使用默认模型"""
    start_time = time.time()
    instance = BGEEmbedder()  # 默认使用 BAAI/bge-m3
    end_time = time.time()
    print(f"\n[Time] 加载 BGE-M3 模型耗时: {end_time - start_time:.2f}s")
    return instance


def test_embedder_initialization(embedder):
    """测试初始化"""
    assert embedder.model is not None
    print("\n[Info] BGE-M3 模型初始化成功")


def test_embed_texts_dense(embedder):
    """测试稠密向量嵌入"""
    texts = ["什么是人工智能？", "机器学习是AI的一个分支"]
    start_time = time.time()
    embeddings = embedder.embed_texts_dense(texts)
    end_time = time.time()
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(texts)
    # BGE-M3 稠密向量维度是 1024
    assert len(embeddings[0]) == 1024
    assert all(isinstance(x, float) for x in embeddings[0])
    print(f"\n[Time] 稠密向量嵌入({len(texts)}个文本)耗时: {end_time - start_time:.4f}s")
    print(f"[Info] 稠密向量维度: {len(embeddings[0])}")


def test_embed_texts_sparse(embedder):
    """测试稀疏向量嵌入"""
    texts = ["什么是人工智能？", "机器学习是AI的一个分支"]
    start_time = time.time()
    embeddings = embedder.embed_texts_sparse(texts)
    end_time = time.time()
    
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(texts)
    # 稀疏向量应该是字典格式 {token_id: weight}
    assert isinstance(embeddings[0], dict)
    assert all(isinstance(k, int) and isinstance(v, float) 
               for k, v in embeddings[0].items())
    print(f"\n[Time] 稀疏向量嵌入({len(texts)}个文本)耗时: {end_time - start_time:.4f}s")
    print(f"[Info] 稀疏向量非零元素数量: {len(embeddings[0])}")


def test_embed_texts_hybrid(embedder):
    """测试混合向量嵌入（稀疏+稠密）"""
    texts = ["什么是人工智能？", "机器学习是AI的一个分支"]
    start_time = time.time()
    results = embedder.embed_texts_hybrid(texts)
    end_time = time.time()
    
    assert isinstance(results, list)
    assert len(results) == len(texts)
    # 检查 EmbedResult 结构
    assert isinstance(results[0], EmbedResult)
    assert isinstance(results[0].dense_embedding, list)
    assert isinstance(results[0].sparse_embedding, dict)
    # 稠密向量维度应该是 1024
    assert len(results[0].dense_embedding) == 1024
    # 稀疏向量应该是字典格式 {token_id: weight}
    assert all(isinstance(k, int) and isinstance(v, float) 
               for k, v in results[0].sparse_embedding.items())
    print(f"\n[Time] 混合向量嵌入({len(texts)}个文本)耗时: {end_time - start_time:.4f}s")
    print(f"[Info] 稠密向量维度: {len(results[0].dense_embedding)}, "
          f"稀疏向量元素数: {len(results[0].sparse_embedding)}")


def test_empty_input(embedder):
    """测试空输入"""
    start_time = time.time()
    # 空列表应该返回空列表
    assert embedder.embed_texts_dense([]) == []
    assert embedder.embed_texts_sparse([]) == []
    assert embedder.embed_texts_hybrid([]) == []
    
    # 空字符串应该能处理
    dense_result = embedder.embed_texts_dense([""])
    sparse_result = embedder.embed_texts_sparse([""])
    hybrid_result = embedder.embed_texts_hybrid([""])
    
    assert len(dense_result) == 1
    assert len(sparse_result) == 1
    assert len(hybrid_result) == 1
    end_time = time.time()
    print(f"\n[Time] 空输入处理耗时: {end_time - start_time:.4f}s")


def test_single_text(embedder):
    """测试单个文本输入"""
    text = "BGE-M3 是强大的多语言嵌入模型"
    start_time = time.time()
    
    dense = embedder.embed_texts_dense([text])
    sparse = embedder.embed_texts_sparse([text])
    hybrid = embedder.embed_texts_hybrid([text])
    
    assert len(dense) == 1
    assert len(sparse) == 1
    assert len(hybrid) == 1
    assert len(dense[0]) == 1024
    assert isinstance(sparse[0], dict)
    assert isinstance(hybrid[0], EmbedResult)
    
    end_time = time.time()
    print(f"\n[Time] 单文本处理耗时: {end_time - start_time:.4f}s")


def test_batch_processing(embedder):
    """测试批量处理"""
    texts = [
        "BGE-M3 是智源研究院发布的强大的多语言嵌入模型",
        "Milvus 是一个高性能的开源向量数据库",
        "今天天气不错，适合出去野餐",
        "机器学习中的稀疏向量可以有效捕捉精确关键词",
    ]
    start_time = time.time()
    results = embedder.embed_texts_hybrid(texts)
    end_time = time.time()
    
    assert len(results) == len(texts)
    # 验证所有结果都有正确的结构
    for result in results:
        assert isinstance(result, EmbedResult)
        assert len(result.dense_embedding) == 1024
        assert isinstance(result.sparse_embedding, dict)
    
    print(f"\n[Time] 批量处理({len(texts)}个文本)耗时: {end_time - start_time:.4f}s")
    print(f"[Info] 平均每个文本耗时: {(end_time - start_time) / len(texts):.4f}s")


def test_custom_model():
    """测试自定义模型初始化"""
    # 注意：这个测试可能会很慢，因为需要加载新模型
    # 可以跳过或使用较小的模型
    pytest.skip("跳过自定义模型测试，避免重复加载模型")


def test_consistency(embedder):
    """测试不同方法返回结果的一致性"""
    text = "测试一致性"
    
    # 从 hybrid 方法获取结果
    hybrid_result = embedder.embed_texts_hybrid([text])[0]
    
    # 从单独的 dense 和 sparse 方法获取结果
    dense_result = embedder.embed_texts_dense([text])[0]
    sparse_result = embedder.embed_texts_sparse([text])[0]
    
    # 稠密向量应该一致
    assert hybrid_result.dense_embedding == dense_result
    
    # 稀疏向量：hybrid 和 sparse 都返回字典格式，应该完全一致
    assert hybrid_result.sparse_embedding == sparse_result
    print("\n[Info] 一致性检查通过：hybrid 和单独方法的结果匹配")

