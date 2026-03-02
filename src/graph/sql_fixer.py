"""
SQL 修复模块

根据执行错误修复 SQL 语句。
"""

import logging

from pydantic import BaseModel, Field

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from llm.llm_base import LLMClientBase
from llm.openai import sql_fix_final_client

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class SQLFixResult(BaseModel):
    """SQL 修复结果"""
    sql: str = Field(..., description="修复后的 SQL 查询语句，以 SELECT 开头")


class SQLFixer:
    """SQL 修复器"""

    def __init__(self, llm_client: LLMClientBase = sql_fix_final_client):
        """
        初始化 SQLFixer

        Args:
            llm_client: LLM 客户端实例，必须实现 LLMClientBase 接口
        """
        if not isinstance(llm_client, LLMClientBase):
            raise TypeError(f"llm_client 必须是 LLMClientBase 的实例，当前类型: {type(llm_client)}")

        self._llm = llm_client
        self._prompt_config = DATAHUNT_CONFIG.PROMPT.sql_fix
        self._system_prompt = self._prompt_config.system_notool
        self._user_template = self._prompt_config.user

    def _build_user_prompt(
        self,
        schemas: str,
        question: str,
        evidence: str,
        original_sql: str,
        validate_error: str,
        execution_error: str = "",
        execution_result: str = "",
        review_comment: str = ""
    ) -> str:
        """构建用户提示词"""
        return self._user_template.format(
            schemas=schemas,
            question=question,
            evidence=evidence if evidence else "<empty>",
            error_sql=original_sql,
            validate_error=validate_error if validate_error else "<empty>",
            execution_error=execution_error if execution_error else "<empty>",
            execution_result=execution_result if execution_result else "<empty>",
            review_comment=review_comment if review_comment else "<empty>"
        )

    async def fix(
        self,
        question: str,
        evidence: str,
        DDL: list[str],
        original_sql: str,
        validate_error: str = "",
        execution_error: str = "",
        execution_result: str = "",
        review_comment: str = ""
    ) -> SQLFixResult:
        """
        根据验证错误或执行错误修复 SQL

        Args:
            question: 用户问题
            evidence: 证据/外部知识
            DDL: 表结构定义列表
            original_sql: 原始 SQL
            validate_error: 验证错误信息（语法、安全等）
            execution_error: 执行错误信息（运行时错误）
            execution_result: 执行结果
            review_comment: review 评审意见

        Returns:
            SQLFixResult: 包含修复后 sql 的结果
        """
        schemas = "\n\n".join(DDL) if DDL else "<empty>"
        user_prompt = self._build_user_prompt(
            schemas=schemas,
            question=question,
            evidence=evidence,
            original_sql=original_sql,
            validate_error=validate_error,
            execution_error=execution_error,
            execution_result=execution_result,
            review_comment=review_comment
        )
        logger.debug(f"[SQLFixer] fix prompt:\n{user_prompt}")

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 使用结构化输出
        response: SQLFixResult = await self._llm.chat_structured_output(
            messages,
            response_format=SQLFixResult
        )

        logger.info(f"[SQLFixer] 修复完成: {response.sql[:100]}...")

        return response
