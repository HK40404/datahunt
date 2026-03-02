"""使用Qwen3-Reranker-0.6B模型对SQL schema进行重排序"""

import logging

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from config import PROJECT_LOGGER_NAME

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class QwenReranker:
    """Qwen3-Reranker-0.6B模型封装类"""

    def __init__(self, model_name: str = "Qwen/Qwen3-Reranker-0.6B", device: str | None = None):
        """
        初始化reranker模型

        Args:
            model_name: 模型名称或路径
            device: 设备，None时自动选择
        """
        self.model_name = model_name
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        # 加载tokenizer和model
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side='left')
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device).eval()

        logger.info(f"✅ 模型加载完成: {model_name} (设备: {self.device})")

        # 设置token IDs
        self.token_true_id = self.tokenizer.convert_tokens_to_ids("yes")
        self.token_false_id = self.tokenizer.convert_tokens_to_ids("no")

        # 设置最大长度
        self.max_length = 1024

        # 设置prefix和suffix tokens
        prefix = "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\".<|im_end|>\n<|im_start|>user\n"
        suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
        self.prefix_tokens = self.tokenizer.encode(prefix, add_special_tokens=False)
        self.suffix_tokens = self.tokenizer.encode(suffix, add_special_tokens=False)

    def _format_instruction(self, instruction: str, query: str, doc: str) -> str:
        """
        格式化输入文本

        Args:
            instruction: 任务指令
            query: 查询文本
            doc: 文档文本

        Returns:
            格式化后的文本
        """
        if instruction is None:
            instruction = 'Given a web search query, retrieve relevant passages that answer the query'
        return f"<Instruct>: {instruction}\n<Query>: {query}\n<Document>: {doc}"

    def _process_inputs(self, pairs: list[str]) -> dict:
        """
        处理输入文本对

        Args:
            pairs: 格式化的文本对列表

        Returns:
            处理后的输入字典
        """
        inputs = self.tokenizer(
            pairs,
            padding=False,
            truncation='longest_first',
            return_attention_mask=False,
            max_length=self.max_length - len(self.prefix_tokens) - len(self.suffix_tokens)
        )

        # 添加prefix和suffix tokens
        for i, ele in enumerate(inputs['input_ids']):
            inputs['input_ids'][i] = self.prefix_tokens + ele + self.suffix_tokens

        # 填充并转换为tensor
        inputs = self.tokenizer.pad(inputs, padding='max_length', return_tensors="pt", max_length=self.max_length)

        # 移动到设备
        for key in inputs:
            inputs[key] = inputs[key].to(self.model.device)

        return inputs

    @torch.no_grad()
    def _compute_logits(self, inputs: dict) -> list[float]:
        """
        计算相关分数

        Args:
            inputs: 处理后的输入字典

        Returns:
            相关分数列表
        """
        batch_scores = self.model(**inputs).logits[:, -1, :]
        true_vector = batch_scores[:, self.token_true_id]
        false_vector = batch_scores[:, self.token_false_id]
        batch_scores = torch.stack([false_vector, true_vector], dim=1)
        batch_scores = torch.nn.functional.log_softmax(batch_scores, dim=1)
        scores = batch_scores[:, 1].exp().tolist()
        return scores

    def rerank(
        self,
        query: str,
        schemas: list[str],
        instruction: str | None = None,
        batch_size: int = 8
    ) -> list[float]:
        """
        对schema列表进行重排序

        Args:
            query: 查询文本
            schemas: schema文本列表
            instruction: 任务指令，默认为None时使用默认指令
            batch_size: 批次大小，默认8，用于控制内存使用

        Returns:
            相关分数列表，与schemas顺序对应
        """
        if not schemas:
            return []

        # 如果数量较少，直接处理
        if len(schemas) <= batch_size:
            pairs = [self._format_instruction(instruction, query, schema) for schema in schemas]
            inputs = self._process_inputs(pairs)
            scores = self._compute_logits(inputs)
            return scores

        # 分批处理
        all_scores = []
        for i in range(0, len(schemas), batch_size):
            batch_schemas = schemas[i:i + batch_size]
            pairs = [self._format_instruction(instruction, query, schema) for schema in batch_schemas]
            inputs = self._process_inputs(pairs)
            batch_scores = self._compute_logits(inputs)
            all_scores.extend(batch_scores)

            # 清理GPU缓存
            if self.device == "cuda":
                torch.cuda.empty_cache()

        return all_scores


# 全局模型实例（延迟加载）
_reranker_instance: QwenReranker | None = None


def rerank_schemas(
    query: str,
    schema_list: list[str],
    instruction: str | None = None,
    model_name: str = "Qwen/Qwen3-Reranker-0.6B",
    batch_size: int = 8
) -> list[float]:
    """
    对SQL schema列表进行重排序，返回相关分数

    Args:
        query: 查询文本
        schema_list: schema文本列表，每个元素是一个表的schema描述
        instruction: 任务指令，默认为None时使用默认指令
        model_name: 模型名称或路径
        batch_size: 批次大小，默认8，用于控制内存使用

    Returns:
        相关分数列表，与schema_list顺序对应，分数范围[0, 1]，越高表示越相关

    Example:
        >>> schemas = [
        ...     "Table: Country\\nColumns:\\n- id: the unique id for countries\\n- name: country name",
        ...     "Table: Match\\nColumns:\\n- id: the unique id for matches\\n- date: the date of the match"
        ... ]
        >>> scores = rerank_schemas("What is the capital of China?", schemas)
        >>> print(scores)  # [0.85, 0.12]
    """
    global _reranker_instance

    # 延迟加载模型
    if _reranker_instance is None or _reranker_instance.model_name != model_name:
        _reranker_instance = QwenReranker(model_name=model_name)

    return _reranker_instance.rerank(query, schema_list, instruction, batch_size=batch_size)
