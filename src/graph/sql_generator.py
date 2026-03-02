"""
SQL 生成器模块

根据问题、数据库Schema和表信息生成SQL语句。
"""

import logging

from pydantic import BaseModel, Field

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from llm.llm_base import LLMClientBase
from llm.openai import sql_generator_client

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class SQLGenerateResult(BaseModel):
    """SQL生成结果"""
    sql: str = Field(..., description="一条SQL查询语句，以SELECT 开头")


class SQLGenerator:
    """SQL生成器"""

    def __init__(self, llm_client: LLMClientBase = sql_generator_client):
        """
        初始化 SQLGenerator

        Args:
            llm_client: LLM 客户端实例，必须实现 LLMClientBase 接口
        """
        if not isinstance(llm_client, LLMClientBase):
            raise TypeError(f"llm_client 必须是 LLMClientBase 的实例，当前类型: {type(llm_client)}")

        self._llm = llm_client
        self._prompt_config = DATAHUNT_CONFIG.PROMPT.sql_generate
        self._system_prompt = self._prompt_config.system
        self._user_template = self._prompt_config.user

    def _build_user_prompt(
        self,
        question: str,
        evidence: str,
        DDL: list[str],
        sql_examples: str = ""
    ) -> str:
        """构建用户提示词"""
        schemas = "\n\n".join(DDL) if DDL else "<empty>"
        return self._user_template.format(
            schemas=schemas,
            question=question,
            evidence=evidence if evidence else "<empty>",
            sql_examples=sql_examples if sql_examples else "<empty>"
        )

    async def generate(
        self,
        question: str,
        evidence: str,
        DDL: list[str],
        sql_examples: str = ""
    ) -> SQLGenerateResult:
        """
        根据问题和Schema生成SQL

        Args:
            question: 用户问题
            evidence: 证据/外部知识
            DDL: 表结构定义列表
            sql_examples: SQL 示例（格式化后的字符串）

        Returns:
            SQLGenerateResult: 包含 sql 的生成结果
        """
        user_prompt = self._build_user_prompt(question, evidence, DDL, sql_examples)
        logger.debug(f"[SQLGenerator] user prompt:\n{user_prompt}")

        messages = [
            Message.system_message(self._system_prompt),
            Message.user_message(user_prompt)
        ]

        # 使用结构化输出
        response = await self._llm.chat_structured_output(
            [m.to_dict() for m in messages],
            response_format=SQLGenerateResult
        )

        return response
