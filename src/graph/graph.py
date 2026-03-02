import logging
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph
from langsmith import Client, traceable, tracing_context

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from context.schema_provider import SchemaProvider
from context.similar_sql_provider import SimilarSQLProvider, SimilarSQLResult
from data_types.message import Message
from graph.rewritter import QueryRewritter
from graph.sql_executor import SQLExecutor
from graph.sql_generator import SQLGenerator
from graph.sql_validator import SQLValidator
from graph.summary import summary_node
from llm.openai import query_rewrite_client, sql_fix_final_client, sql_generator_client

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class State(TypedDict):
    question: str  # 改写后的问题
    messages: list[Message]  # 对话历史
    evidence: str  # 证据/外部知识
    database: str  # 数据库名称
    generated_sql: str
    matched_tables: list[str]  # Schema Linking结果：匹配到的表列表
    DDL: list[str]
    exec_result: list[dict[str, Any]]  # SQL 执行结果
    exec_error: str  # 执行错误（运行时错误）
    validate_error: str | None  # 验证错误（语法、安全等）
    review_result: bool  # review 评审结果（True=通过，False=失败）
    review_comment: str  # review 评审意见
    fix_count: int  # 修复次数
    answer: str | None  # 最终答案（summary 节点生成）


class DataHuntGraph:
    MAX_FIX_COUNT = 2

    def __init__(self, use_agent_fix: bool = True):
        self._use_agent_fix = use_agent_fix
        self._graph = self._build_graph()

        # 初始化各个组件
        self._schema_provider = SchemaProvider()
        self._query_rewritter = QueryRewritter(client=query_rewrite_client)
        self._sql_generator = SQLGenerator(llm_client=sql_generator_client)
        self._sql_validator = SQLValidator(database_type="mysql")
        self._sql_executor = SQLExecutor()  # SQL 执行器
        self._similar_sql_provider = SimilarSQLProvider(top_k=10)

    def _should_validate_fail(self, state: State) -> str:
        """
        判断验证是否失败
        返回: "sql_fix" 表示需要修复, "sql_execute" 表示继续执行
        """
        if state["validate_error"]:
            return "sql_fix"
        return "sql_execute"

    def _should_execute_fail(self, state: State) -> str:
        """
        判断执行是否失败
        返回: "sql_fix" 表示需要修复, "summary" 表示继续到 summary 节点
        """
        exec_error = state.get("exec_error", "")
        exec_result = state.get("exec_result", [])
        if exec_error or not exec_result:
            return "sql_fix"
        return "summary"

    def _should_fix_complete(self, state: State) -> str:
        """修复完成后判断下一步"""
        # 如果 fix_count 已达上限，降级完成，去 summary
        fix_count = state.get("fix_count", 0)
        if fix_count >= self.MAX_FIX_COUNT:
            return "summary"
        # 否则修复成功，回 validator 重新验证
        return "validate"

    def _build_graph(self):
        graph = StateGraph(State)
        graph.add_node("query_rewrite", self.query_rewrite)
        graph.add_node("schema_link", self.schema_link)
        graph.add_node("sql_generator", self.generate_sql)
        graph.add_node("sql_validator", self.validate_sql)
        graph.add_node("sql_execute", self.execute_sql)
        graph.add_node("sql_fix", self.fix_sql)
        graph.add_node("summary", self.summarize)

        graph.add_edge(START, "query_rewrite")
        graph.add_edge("query_rewrite", "schema_link")
        graph.add_edge("schema_link", "sql_generator")
        graph.add_edge("sql_generator", "sql_validator")

        # validator 条件边：验证失败 → sql_fix，否则 → sql_execute
        graph.add_conditional_edges(
            "sql_validator", self._should_validate_fail, {"sql_fix": "sql_fix", "sql_execute": "sql_execute"}
        )

        # execute 条件边：执行失败/结果为空 → sql_fix，否则 → summary
        graph.add_conditional_edges(
            "sql_execute", self._should_execute_fail, {"sql_fix": "sql_fix", "summary": "summary"}
        )

        # summary 节点：直接结束
        graph.add_edge("summary", END)

        # sql_fix 条件边：修复成功回 validator 重新验证，降级后直接结束
        graph.add_conditional_edges("sql_fix", self._should_fix_complete, {"validate": "sql_validator", "end": END})
        return graph.compile()

    # ===== Graph Nodes =====
    async def query_rewrite(self, state: State) -> dict:
        """
        Query Rewrite 节点：将对话历史总结为一个独立问题

        Args:
            state: 包含以下字段:
                - messages: 对话历史消息列表
                - evidence: 外部知识

        Returns:
            部分状态更新，包含 question 字段（改写后的问题）
        """
        messages: list[Message] = state.get("messages", [])
        evidence = state.get("evidence", "")

        # 调用 QueryRewritter 改写问题
        result = await self._query_rewritter.rewrite_from_messages(messages, evidence)

        logger.debug(
            f"[query_rewrite] 原始对话: {messages[-1].content if messages else ''} ；改写后问题: {result.query}"
        )

        return {"question": result.query}

    async def schema_link(self, state: State) -> dict:
        """
        Schema Linking: 从向量数据库检索相关表并rerank返回top 10表

        Args:
            state: 包含以下字段:
                - question: 改写后的问题
                - database: 数据库名称

        Returns:
            部分状态更新，包含 matched_tables 和 DDL 字段
        """
        question = state["question"]
        database = state.get("database", "bird")

        # 调用SchemaProvider进行Schema Linking
        matched_tables, ddls = await self._schema_provider.schema_link(question, database)

        return {"matched_tables": matched_tables, "DDL": ddls}

    def _format_sql_examples(self, results: list[SimilarSQLResult]) -> str:
        """将相似 SQL 结果格式化为 prompt 所需格式"""
        lines = []
        for i, r in enumerate(results, 1):
            lines.append(f"question {i}: {r.original_question}")
            lines.append(f"evidence {i}: {r.evidence if r.evidence else '<empty>'}")
            lines.append(f"answer sql {i}: {r.sql}")
            lines.append("")  # 空行分隔
        return "\n".join(lines)

    async def generate_sql(self, state: State) -> dict:
        """
        SQL生成节点：根据问题、Schema信息生成SQL

        Args:
            state: 包含question、evidence、DDL等字段

        Returns:
            部分状态更新，包含 generated_sql 字段
        """
        question = state["question"]
        evidence = state["evidence"]
        DDL = state.get("DDL", [])

        # 获取相似 SQL 示例
        similar_results = await self._similar_sql_provider.find_similar_sql(question, top_k=10)
        sql_examples = self._format_sql_examples(similar_results)

        result = await self._sql_generator.generate(
            question=question, evidence=evidence, DDL=DDL, sql_examples=sql_examples
        )

        return {"generated_sql": result.sql.strip(), "fix_count": 0}

    async def validate_sql(self, state: State) -> dict:
        """
        SQL校验节点：验证生成的SQL语法和安全性

        Args:
            state: 包含generated_sql字段

        Returns:
            部分状态更新，包含 validate_error 字段
        """
        sql = state["generated_sql"]

        result = self._sql_validator.validate(sql)

        if result["is_valid"]:
            return {"validate_error": None}
        else:
            return {"validate_error": result["error_message"]}

    async def execute_sql(self, state: State) -> dict:
        """
        SQL执行节点：实际执行SQL，返回结果或错误

        Args:
            state: 包含 generated_sql、database 等字段

        Returns:
            部分状态更新，包含 exec_result 和 exec_error 字段
        """
        sql = state["generated_sql"]
        database = state.get("database", "bird")

        success, results, error = self._sql_executor.execute_query(database, sql)

        if success:
            return {"exec_result": results, "exec_error": ""}
        else:
            return {"exec_result": [], "exec_error": error}

    async def fix_sql(self, state: State) -> dict:
        """
        SQL修复节点：使用 SQLAgent 或 SQLFixer 修复验证或执行失败的 SQL

        Args:
            state: 包含 generated_sql、validate_error/exec_error、DDL 等字段

        Returns:
            部分状态更新，包含 generated_sql、original_sql、fix_count 字段
        """
        fix_count = state.get("fix_count", 0)

        # 如果已到上限，降级返回原 SQL，直接结束
        if fix_count >= self.MAX_FIX_COUNT:
            logger.warning(f"[sql_fix] 修复次数已达上限 {self.MAX_FIX_COUNT}，降级返回原 SQL")
            return {"generated_sql": state["generated_sql"], "validate_error": None, "exec_error": ""}

        question = state["question"]
        evidence = state["evidence"]
        DDL = state.get("DDL", [])
        current_sql = state["generated_sql"]
        validate_error = state["validate_error"] or ""
        exec_error = state["exec_error"] or ""
        database = state.get("database", "bird")
        exec_result = state.get("exec_result", [])

        if self._use_agent_fix:
            # 使用 SQLAgent (ReAct 模式)
            from agent.agent.sql_agent import SQLAgent, SQLAgentState

            agent_state = SQLAgentState(
                question=question,
                evidence=evidence,
                DDL=DDL,
                original_sql=current_sql,
                validate_error=validate_error,
                execution_error=exec_error,
                execution_result=exec_result,
                database=database,
            )
            agent = SQLAgent(llm_client=sql_fix_final_client, max_execute_count=10)
            try:
                fixed_sql = await agent.run(agent_state)
            except RuntimeError as e:
                logger.error(f"[sql_fix] 修复失败，降级返回原 SQL: {e}")
                fixed_sql = current_sql
        else:
            # 使用 SQLFixer (简单 LLM 修复)
            from graph.sql_fixer import SQLFixer

            execution_result_str = str(exec_result) if exec_result else ""
            result = await SQLFixer().fix(
                question=question,
                evidence=evidence,
                DDL=DDL,
                original_sql=current_sql,
                validate_error=validate_error,
                execution_error=exec_error,
                execution_result=execution_result_str,
            )
            fixed_sql = result.sql

        return {
            "generated_sql": fixed_sql.strip(),
            "validate_error": None,
            "exec_error": "",
            "fix_count": fix_count + 1,
            "exec_result": [],  # 清空执行结果
        }

    async def summarize(self, state: State) -> dict:
        """
        Summary 节点：根据查询结果生成自然语言答案

        Args:
            state: 包含 question、generated_sql、exec_result、validate_error、exec_error 字段

        Returns:
            部分状态更新，包含 answer 字段
        """
        question = state.get("question", "")
        generated_sql = state.get("generated_sql", "")
        exec_result = state.get("exec_result", [])
        validate_error = state.get("validate_error")
        exec_error = state.get("exec_error", "")

        result = await summary_node.generate(
            question=question,
            generated_sql=generated_sql,
            exec_result=exec_result,
            validate_error=validate_error,
            exec_error=exec_error,
        )

        return {"answer": result}


datahunt_graph = DataHuntGraph()
langsmith_client = Client(
    api_key=DATAHUNT_CONFIG.LANGSMITH_API_KEY,
    api_url=DATAHUNT_CONFIG.LANGSMITH_BASE_URL,
)


@traceable
async def _do_text_to_sql(state: State) -> State:
    return await datahunt_graph._graph.ainvoke(state)


async def text_to_sql(state: State) -> State:
    with tracing_context(enabled=True):
        return await _do_text_to_sql(
            state,
            langsmith_extra={"client": langsmith_client, "project_name": DATAHUNT_CONFIG.LANGSMITH_PROJECT_NAME},
        )
