import time

import pytest

from src.embed.transformer_embedder import TransformerEmbedder


@pytest.fixture(scope="module")
def embedder():
    """创建一个共享的 embedder 实例，使用默认模型"""
    start_time = time.time()
    instance = TransformerEmbedder()  # 默认使用 Qwen/Qwen3-Embedding-0.6B
    end_time = time.time()
    print(f"\n[Time] 加载默认模型 {instance.model_name} 耗时: {end_time - start_time:.2f}s")
    return instance

def test_embedder_initialization(embedder):
    """测试初始化"""
    assert embedder.model_name == TransformerEmbedder.DEFAULT_MODEL
    assert embedder.dimension > 0
    assert embedder.device in ["cuda", "cpu", "mps"]
    print(f"\n[Info] 模型维度: {embedder.dimension}, 设备: {embedder.device}")

def test_embed_query(embedder):
    """测试单查询向量化"""
    query = "什么是人工智能？"
    start_time = time.time()
    embedding = embedder.embed_query(query)
    end_time = time.time()
    assert isinstance(embedding, list)
    assert len(embedding) == embedder.dimension
    assert all(isinstance(x, float) for x in embedding)
    print(f"\n[Time] 单查询向量化耗时: {end_time - start_time:.4f}s")

def test_embed_documents(embedder):
    """测试批量文档向量化"""
    docs = ["机器学习", "深度学习", "自然语言处理"]
    start_time = time.time()
    embeddings = embedder.embed_documents(docs)
    end_time = time.time()
    assert isinstance(embeddings, list)
    assert len(embeddings) == len(docs)
    for emb in embeddings:
        assert len(emb) == embedder.dimension
    print(f"\n[Time] 批量文档({len(docs)}个)向量化耗时: {end_time - start_time:.4f}s")

def test_tokenizer_functions(embedder):
    """测试 tokenizer 功能"""
    text = "Hello, 世界"
    start_time = time.time()
    tokens = embedder.tokenize(text)
    end_time = time.time()
    assert isinstance(tokens, list)
    assert len(tokens) > 0
    
    count = embedder.count_tokens(text)
    assert count == len(tokens)
    print(f"\n[Time] Tokenizer 处理耗时: {end_time - start_time:.4f}s")

def test_model_switching():
    """测试模型切换和内存释放"""
    # 重新创建一个用于切换测试的实例，避免影响全局 fixture
    embedder = TransformerEmbedder()
    old_model_name = embedder.model_name
    
    # 切换到一个较小的模型以节省时间
    start_time = time.time()
    embedder.load_model("BAAI/bge-small-en-v1.5")
    end_time = time.time()
    
    assert embedder.model_name == "BAAI/bge-small-en-v1.5"
    assert embedder.model_name != old_model_name
    print(f"\n[Time] 切换模型耗时: {end_time - start_time:.2f}s")
    
    # 再次清理
    embedder._release_model()
    assert embedder._model is None
    assert embedder.model_name is None

def test_query_instruction():
    """测试查询指令"""
    # Qwen3 系列模型支持指令
    embedder = TransformerEmbedder(
        query_instruction="Represent this sentence for searching: "
    )
    start_time = time.time()
    embedding = embedder.embed_query("How does Text-to-SQL work?")
    end_time = time.time()
    assert len(embedding) == embedder.dimension
    print(f"\n[Time] 带指令的查询向量化耗时: {end_time - start_time:.4f}s")

def test_empty_input(embedder):
    """测试空输入"""
    start_time = time.time()
    assert embedder.embed_documents([]) == []
    
    # 模型应该能处理空字符串
    embedding = embedder.embed_query("")
    end_time = time.time()
    assert len(embedding) == embedder.dimension
    print(f"\n[Time] 空输入处理耗时: {end_time - start_time:.4f}s")
