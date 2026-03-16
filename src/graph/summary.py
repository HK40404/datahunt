"""
Summary 节点模块

根据 SQL 查询结果生成面向用户的自然语言答案。
"""

import logging
from typing import Any

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from llm.llm_base import LLMClientBase
from llm.openai import sql_generator_client

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class SummaryNode:
    """Summary 节点：根据查询结果生成自然语言答案"""

    def __init__(self, llm_client: LLMClientBase = sql_generator_client):
        self._llm = llm_client
        self._prompt_config = DATAHUNT_CONFIG.PROMPT.sql_summary
        self._system_prompt = self._prompt_config.system
        self._system_prompt_long = self._prompt_config.system_long_answer
        self._user_template = self._prompt_config.user

    def _build_user_prompt(self, question: str, generated_sql: str, exec_result: list[dict[str, Any]]) -> str:
        """构建用户提示词"""
        result_str = str(exec_result) if exec_result else "<empty>"
        return self._user_template.format(question=question, generated_sql=generated_sql, exec_result=result_str)

    async def generate(
        self,
        question: str,
        generated_sql: str,
        exec_result: list[dict[str, Any]],
        validate_error: str | None,
        exec_error: str,
    ) -> str:
        """
        生成自然语言答案

        Args:
            question: 用户问题
            generated_sql: 生成的 SQL
            exec_result: SQL 执行结果
            validate_error: 验证错误
            exec_error: 执行错误

        Returns:
            自然语言答案字符串
        """
        # 错误场景：存在验证错误或执行错误
        if validate_error or exec_error:
            return "查询错误达最大次数，请稍后重试。"

        # 成功场景但无返回数据
        if not exec_result:
            return "未找到相关数据。"

        # 成功场景：根据结果生成答案
        result_str = str(exec_result) if exec_result else ""

        # 根据结果长度选择 system prompt
        if len(result_str) > 300 and exec_result:
            system_prompt = self._system_prompt_long
        else:
            system_prompt = self._system_prompt

        user_prompt = self._build_user_prompt(question, generated_sql, exec_result)
        logger.debug(f"[SummaryNode] system prompt:\n{system_prompt}")
        logger.debug(f"[SummaryNode] user prompt:\n{user_prompt}")

        messages = [Message.system_message(system_prompt), Message.user_message(user_prompt)]

        response = await self._llm.chat([m.to_dict() for m in messages])
        return response.content if hasattr(response, "content") else str(response)


# 全局实例
summary_node = SummaryNode()
