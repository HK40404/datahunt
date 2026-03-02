
from FlagEmbedding import BGEM3FlagModel

from .base_embedder import Embedder, EmbedResult


class BGEEmbedder(Embedder):
    """BGE-M3 嵌入模型实现（单例模式）"""

    _instance = None
    _model = None

    def __new__(cls, model_name: str = 'BAAI/bge-m3', use_fp16: bool = True):
        """单例模式：模型只加载一次"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 第一次创建时加载模型
            print(f"Loading BGE-M3 model: {model_name}")
            cls._model = BGEM3FlagModel(model_name, use_fp16=use_fp16)
        return cls._instance

    def __init__(self, model_name: str = 'BAAI/bge-m3', use_fp16: bool = True):
        """单例模式，__init__ 只执行一次"""
        # 单例模式下，model 在 __new__ 中已加载
        self.model = self.__class__._model

    def embed_texts_hybrid(self, texts: list[str]) -> list[EmbedResult]:
        """将文本embed为稀疏、稠密两种向量"""
        if not texts:
            return []
        output = self.model.encode(texts, return_dense=True, return_sparse=True)

        results = []
        for i in range(len(texts)):
            # 转换稠密向量：numpy array -> list
            dense_vec = output['dense_vecs'][i].tolist()

            # 转换稀疏向量：dict with str keys -> dict with int keys
            sparse_dict = {int(k): float(v) for k, v in output['lexical_weights'][i].items()}

            results.append(EmbedResult(
                sparse_embedding=sparse_dict,
                dense_embedding=dense_vec
            ))

        return results

    def embed_texts_sparse(self, texts: list[str]) -> list[dict[int, float]]:
        """将文本embed为稀疏向量，输出格式为{token_id: weight}列表"""
        if not texts:
            return []
        output = self.model.encode(texts, return_sparse=True)

        results = []
        for i in range(len(texts)):
            # 转换 key 从 str 到 int
            sparse_dict = {int(k): float(v) for k, v in output['lexical_weights'][i].items()}
            results.append(sparse_dict)

        return results

    def embed_texts_dense(self, texts: list[str]) -> list[list[float]]:
        """将文本embed为稠密向量"""
        if not texts:
            return []
        output = self.model.encode(texts, return_dense=True)

        results = []
        for i in range(len(texts)):
            # 转换 numpy array 到 list
            dense_vec = output['dense_vecs'][i].tolist()
            results.append(dense_vec)

        return results

