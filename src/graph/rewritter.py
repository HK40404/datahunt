"""
Query Rewriter 模块

根据用户的问题和提供的evidence，改写为适合检索数据表以及生成SQL的问题。
支持使用任何实现了 LLMClientBase 接口的 LLM 客户端。
"""

import logging
from datetime import datetime

from pydantic import BaseModel, Field

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from llm.llm_base import LLMClientBase

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class RewriteQueryResponse(BaseModel):
    query: str = Field(..., description="改写后的查询，用于搜索向量数据库")


class QueryRewritter:
    """
    Query Rewriter

    将用户的提问结合evidence改写为适合检索数据表以及生成SQL的问题。

    使用示例:
    ```python
    from graph.rewritter import QueryRewriter
    from llm.gemini import gemini_client
    from llm.openai import openai_client

    # 使用 Gemini 客户端
    rewriter = QueryRewriter(client=gemini_client)
    result = await rewriter.rewrite(
        question="查询比利时的人口",
        evidence="比利时是欧洲的一个国家"
    )
    print(f"推理过程: {result.reasoning}")
    print(f"改写后的问题: {result.query}")

    # 使用 OpenAI 客户端
    rewriter = QueryRewriter(client=openai_client)
    ```
    """

    def __init__(self, client: LLMClientBase):
        """
        初始化 Query Rewriter

        Args:
            client: LLM 客户端实例，必须实现 LLMClientBase 接口
        """
        if not isinstance(client, LLMClientBase):
            raise TypeError(
                f"client 必须是 LLMClientBase 的实例，当前类型: {type(client)}"
            )

        self.client = client

        # 从配置中获取 prompt
        query_rewriter_prompt = DATAHUNT_CONFIG.PROMPT.query_rewritter
        self.system_prompt = query_rewriter_prompt.system
        self.user_prompt_template = query_rewriter_prompt.user

    async def rewrite_from_messages(
        self, messages: list[Message], evidence: str = ""
    ) -> RewriteQueryResponse:
        """
        根据对话历史改写用户问题

        Args:
            messages: 对话历史消息列表
            evidence: 提供的evidence（外部知识、缩写定义、计算公式或特定业务逻辑）

        Returns:
            RewriteQueryResponse: 包含改写后问题的结构化响应
        """
        # 分离 latest_query 和 conversation_history
        if messages:
            latest_query = (
                messages[-1].content if messages[-1].role.value == "user" else ""
            )
            if not latest_query:
                logger.error("[Rewritter] 对话历史最后一条消息不是用户问题，终止流程")
                raise ValueError("latest query empty")
            conversation_history_messages = messages[:-1]
        else:
            logger.error("[Rewritter] 对话历史为空，终止流程")
            raise ValueError("messages empty")

        # 格式化对话历史（除最后一条消息外）
        conversation_history = [m.to_dict() for m in conversation_history_messages]
        history_str = str(conversation_history) if conversation_history else "<empty>"

        # 获取当前时间，精确到分钟
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")

        # 格式化 user prompt
        user_prompt = self.user_prompt_template.format(
            conversation_history=history_str,
            latest_query=latest_query,
            current_time=current_time,
            evidence=evidence if evidence else "<empty>",
        )

        # 构建消息列表
        messages_list = [
            Message.system_message(self.system_prompt),
            Message.user_message(user_prompt),
        ]

        # 使用结构化输出调用 LLM
        response = await self.client.chat_structured_output(
            [m.to_dict() for m in messages_list], response_format=RewriteQueryResponse
        )

        return response
