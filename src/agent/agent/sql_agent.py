"""
SQL Agent

基于 ReAct 模式的 SQL 修复 Agent，使用 sql_fix prompt 修复错误的 SQL。

支持调用 SelectSQLTool 工具查询数据库，或直接输出 SQL。
"""

import json
import logging
import re
from typing import Any

from pydantic import BaseModel

from agent.tool.base_tool import ToolSet
from agent.tool.sql_fix_tools import SelectSQLTool
from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message
from llm.llm_base import LLMClientBase, LLMToolCall
from llm.openai import OpenAIClient, sql_fix_client, sql_fix_final_client

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

MAX_REVIEW_LENGTH = 1024


class SQLAgentState(BaseModel):
    """SQL Agent 状态"""
    question: str
    evidence: str
    DDL: list[str]
    database: str
    execute_count: int = 0

    # 修复模式字段
    original_sql: str = ""  # 最近一次报错的 SQL
    validate_error: str = ""
    execution_error: str = ""
    execution_result: list[dict[str, Any]] = []
    review_comment: str = ""  # review 评审意见


class SQLAgent:
    """SQL Agent (ReAct 模式)，修复模式"""

    def __init__(
        self,
        llm_client: LLMClientBase = sql_fix_client,
        max_execute_count: int = 10
    ):
        """
        初始化 SQLAgent

        Args:
            llm_client: LLM 客户端
            max_execute_count: 最大执行次数（内部工具调用轮次）
        """
        self._llm = llm_client
        self._max_execute_count = max_execute_count
        self.tool_calls: list[LLMToolCall] = []
        self._messages: list[Message] = []  # 持有对话历史
        self._final_client = sql_fix_final_client
        self._tool_set = ToolSet([SelectSQLTool])

    def _extract_sql_from_content(self, content: str) -> str | None:
        """从 LLM 响应内容中解析 SQL（JSON 格式）"""
        try:
            data = json.loads(content)
            if "sql" in data:
                return data["sql"]
        except json.JSONDecodeError:
            pass

        match = re.search(r'```(?:json)?\s*\n?\s*\{\s*"sql"\s*:\s*"([^"]+)"\s*\}\s*```', content, re.DOTALL)
        if match:
            return match.group(1)

        match = re.search(r'\{\s*"sql"\s*:\s*"([^"]+)"\s*\}', content, re.DOTALL)
        if match:
            return match.group(1)

        return None

    def _build_prompt(self, state: SQLAgentState) -> tuple[str, str]:
        """
        构建 fix 模式的 prompt

        Args:
            state: SQLAgentState

        Returns:
            (system_prompt, user_prompt)
        """
        schemas = "\n\n".join(state.DDL) if state.DDL else "<empty>"

        # 修复模式：使用 sql_fix prompt
        prompt_config = DATAHUNT_CONFIG.PROMPT.sql_fix

        # 原始错误 SQL
        error_sql = state.original_sql if state.original_sql else "<empty>"
        result_text = str(state.execution_result)[:MAX_REVIEW_LENGTH] if state.execution_result else "<empty>"


        user_prompt = prompt_config.user.format(
            schemas=schemas,
            question=state.question,
            evidence=state.evidence if state.evidence else "<empty>",
            error_sql=error_sql,
            validate_error=state.validate_error if state.validate_error else "<empty>",
            execution_error=state.execution_error if state.execution_error else "<empty>",
            execution_result=result_text,
            review_comment=state.review_comment if state.review_comment else "<empty>",
        )

        system_prompt = prompt_config.system.replace(
            "{sql_query_tool}", SelectSQLTool.name()
        ).replace(
            "{sql_output_tool}", "直接输出 JSON 格式的 SQL 答案"
        )

        return system_prompt, user_prompt

    def execute_tool(self, tool_call: LLMToolCall, database: str) -> str:
        """执行单个工具调用"""
        tool_class = self._tool_set.get_tool(tool_call.name)
        if tool_class:
            return tool_class.invoke(**tool_call.arguments, database=database)
        return f"Unknown tool: {tool_call.name}"

    async def think(self, state: SQLAgentState, use_final: bool = False) -> str | None:
        """
        ReAct Think: 分析状态，决定是否需要行动

        Args:
            state: 状态
            use_final: 是否使用 final_client（最后一次循环，不调用工具）

        Returns:
            str: 如果直接返回 SQL 则返回 SQL，否则返回 None 表示需要执行工具
        """
        # 如果 memory 为空，先添加 system 和 user
        if not self._messages:
            system_prompt, user_prompt = self._build_prompt(state)
            self._messages.append(Message.system_message(system_prompt))
            self._messages.append(Message.user_message(user_prompt))

        try:
            if use_final:
                # 最后一次循环，必须输出SQL
                response = await self._final_client.chat(
                    [msg.to_dict() for msg in self._messages]
                )
                self._messages.append(Message.assistant_message(response.content or ""))

                if response.content:
                    sql = self._extract_sql_from_content(response.content)
                    if sql:
                        return sql
            else:
                response = await self._llm.chat(
                    [msg.to_dict() for msg in self._messages],
                    tools=self._tool_set.get_schemas()
                )

                self.tool_calls = OpenAIClient.parse_tool_calls(response.raw_response)

                tool_calls_data = None
                if self.tool_calls:
                    tool_calls_data = [
                        {"id": tc.id, "type": "function", "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)}}
                        for tc in self.tool_calls
                    ]
                self._messages.append(Message.assistant_message(response.content or "", tool_calls=tool_calls_data))

                if not self.tool_calls:
                    sql = self._extract_sql_from_content(response.content)
                    if sql:
                        return sql

        except Exception as e:
            logger.error(f"[SQLAgent] think 错误: {e}")
            return None

        return None

    async def act(self, state: SQLAgentState) -> None:
        """ReAct Act: 执行工具调用"""
        if not self.tool_calls:
            return

        for tool in self.tool_calls:
            tool_result = self.execute_tool(tool, state.database)
            self._messages.append(Message.tool_message(tool_result, tool_call_id=tool.id))

    async def run(self, state: SQLAgentState) -> str:
        """
        ReAct 主循环：think -> act

        LLM 可以调用工具查询数据库，或直接输出 SQL。
        最后一次循环使用 final_client，不传 tools，直接输出 SQL。

        Args:
            state: SQLAgentState

        Returns:
            SQL 语句

        Raises:
            RuntimeError: 超过最大次数仍未修复 SQL
        """
        self._messages = []
        self.tool_calls = []

        # 获取 final_prompt
        prompt_config = DATAHUNT_CONFIG.PROMPT.sql_fix
        final_prompt = getattr(prompt_config, "final_prompt", "")

        should_end = False
        for i in range(self._max_execute_count):
            if i == self._max_execute_count - 1:
                logger.warning("[SQLAgent] run: 达到最大轮次，要求直接输出SQL")
                should_end = True

            # 最后一次循环：添加 final_prompt
            if should_end and final_prompt:
                self._messages.append(Message.user_message(final_prompt))

            # Think
            sql = await self.think(state, use_final=should_end)

            if sql:
                return sql

            if should_end:
                break

            if self.tool_calls:
                await self.act(state)
            else:
                logger.warning("[SQLAgent] run: 没有工具调用，要求直接输出SQL")
                should_end = True

            state.execute_count = i + 1

        # 超过最大次数
        logger.error("[SQLAgent] 修复失败: 返回原 SQL: {state.original_sql}")
        return state.original_sql
