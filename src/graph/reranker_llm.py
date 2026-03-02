"""
Schema Reranker LLM 模块

使用大模型对多个数据表schema进行rerank，根据与查询的相关性进行排序。
支持使用任何实现了 LLMClientBase 接口的 LLM 客户端。
"""

import logging

from pydantic import BaseModel, Field

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from llm.llm_base import LLMClientBase

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class RerankResult(BaseModel):
    """Schema重排序结果，包含排序后的schema index列表"""
    schema_list: list[int] = Field(..., description="排序后的schema索引列表，按相关性评分从高到低排序，包含前10个schema的编号")


class LLMReranker:
    """

    使用大模型对多个数据表schema进行rerank，根据与查询的相关性进行排序。

    使用示例:
    ```python
    from graph.reranker_llm import LLMReranker
    from llm.gemini import gemini_client
    from llm.openai import openai_client

    # 使用 Gemini 客户端
    reranker = LLMReranker(client=gemini_client)
    result = await reranker.rerank(
        query="查询比利时的人口",
        schemas={
            "country": "Table: Country\nColumns:\n- id: the unique id for countries\n- name: country name",
            "match": "Table: Match\nColumns:\n- id: the unique id for matches\n- date: the date of the match"
        }
    )
    print(f"排序后的schema索引: {result.schema_list}")

    # 使用 OpenAI 客户端
    reranker = LLMReranker(client=openai_client)
    ```
    """

    def __init__(self, client: LLMClientBase):
        """
        初始化 LLMReranker

        Args:
            client: LLM 客户端实例，必须实现 LLMClientBase 接口
        """
        if not isinstance(client, LLMClientBase):
            raise TypeError(f"client 必须是 LLMClientBase 的实例，当前类型: {type(client)}")

        self.client = client

        # 从配置中获取 prompt
        schema_rerank_prompt = DATAHUNT_CONFIG.PROMPT.schema_rerank
        self.system_prompt = schema_rerank_prompt.system
        self.user_prompt_template = schema_rerank_prompt.user

    def _format_schemas(self, schemas: dict) -> str:
        """
        格式化schemas为字符串，并打印日志

        Args:
            schemas: schema字典，key为schema_name，value为schema文本

        Returns:
            格式化后的schemas字符串
        """
        schema_items = list(schemas.items())
        schemas_text = "\n\n".join([
            f"Schema {i}:\n{schema_content}"
            for i, (_, schema_content) in enumerate(schema_items)
        ])

        # 在一行内打印所有Schema的名字和index
        schema_info = ", ".join([f"{i}: {schema_name}" for i, (schema_name, _) in enumerate(schema_items)])
        logger.debug(f"格式化Schemas: {schema_info}")

        return schemas_text

    async def rerank(
        self,
        query: str,
        schemas: dict
    ) -> RerankResult:
        """
        对schema字典进行rerank

        Args:
            query: 查询文本
            schemas: schema字典，key为schema_name，value为schema文本

        Returns:
            RerankResult: 包含排序后的schema索引列表（只包含前10个）
        """
        if not schemas:
            return RerankResult(schema_list=[])

        # 格式化 schemas 为字符串
        schemas_text = self._format_schemas(schemas)

        # 格式化 user prompt
        user_prompt = self.user_prompt_template.format(
            query=query,
            schemas=schemas_text
        )

        # 构建消息列表
        messages = [
            Message.system_message(self.system_prompt),
            Message.user_message(user_prompt)
        ]

        # 使用结构化输出调用 LLM
        response = await self.client.chat_structured_output(
            [m.to_dict() for m in messages],
            response_format=RerankResult
        )

        # 后处理：去重 + 有效性检查 + 数量调整
        input_count = len(schemas)
        original_count = len(response.schema_list)

        # 有效性检查：过滤无效索引
        valid_indices = [idx for idx in response.schema_list if 0 <= idx < input_count]
        invalid_indices = [idx for idx in response.schema_list if idx < 0 or idx >= input_count]

        if invalid_indices:
            logger.warning(f"[后处理] LLM返回了 {len(invalid_indices)} 个无效索引: {invalid_indices}")

        # 去重：保持顺序
        seen_indices = set()
        unique_indices = []
        for idx in valid_indices:
            if idx not in seen_indices:
                seen_indices.add(idx)
                unique_indices.append(idx)

        # 数量调整：补齐或截断到10个
        if len(unique_indices) < 10:
            # 不足10个，按照输入顺序补齐（不重复）
            for idx in range(input_count):
                if len(unique_indices) >= 10:
                    break
                if idx not in seen_indices:
                    unique_indices.append(idx)
            logger.info(f"[后处理] LLM返回 {original_count} 个有效schema，补齐到 {len(unique_indices)} 个")
        elif len(unique_indices) > 10:
            # 超过10个，截断为10个
            unique_indices = unique_indices[:10]
            logger.info(f"[后处理] LLM返回 {original_count} 个有效schema，截断到 {len(unique_indices)} 个")
        # 如果刚好是10个，不需要处理

        response.schema_list = unique_indices
        return response
