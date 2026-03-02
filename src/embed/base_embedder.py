from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class EmbedResult:
    sparse_embedding: dict[int, float]
    dense_embedding: list[float]

class Embedder(ABC):
    @abstractmethod
    def embed_texts_hybrid(self, texts: list[str]) -> list[EmbedResult]:
        """将文本embed为稀疏、稠密两种向量"""
        pass

    @abstractmethod
    def embed_texts_sparse(self, texts: list[str]) -> list[dict[int, float]]:
        """将文本embed为稀疏向量，输出格式为{token_id: weight}列表"""
        pass

    @abstractmethod
    def embed_texts_dense(self, texts: list[str]) -> list[list[float]]:
        """将文本embed为稠密向量"""
        pass

