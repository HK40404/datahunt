"""
SQL Fix 工具集

包含 SQL 执行相关的工具。
类方法设计，无需实例化。
"""

from typing import Any

from pydantic import BaseModel, Field

from agent.tool.base_tool import BaseTool
from graph.sql_executor import SQLExecutor
from graph.sql_validator import SQLValidator


class ExecuteSQLArgs(BaseModel):
    """执行 SQL 参数"""
    sql: str = Field(..., description="要执行的 SQL 语句")


class SelectSQLTool(BaseTool):
    """执行 SQL 工具"""

    @classmethod
    def name(cls) -> str:
        return "select_tool"

    @classmethod
    def description(cls) -> str:
        return "在生成 SQL 查询之前，可以使用此工具来理解数据库结构。它可以获取指定表的列名、数据类型、外键关系以及几行样本数据。样本数据对于理解某些字段的具体取值（如状态码、类别名称）至关重要"

    @classmethod
    def parameters(cls) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "sql": {
                    "type": "string",
                    "description": "The SQL statement to execute"
                }
            },
            "required": ["sql"]
        }

    @classmethod
    def invoke(cls, **kwargs) -> str:
        """执行并验证 SQL 语句"""
        sql = kwargs["sql"]
        database = kwargs["database"]

        validator = SQLValidator(database_type="mysql")
        validate_result = validator.validate(sql)

        if not validate_result["is_valid"]:
            return f"Validation Error: {validate_result['error_message']}"

        executor = SQLExecutor(database=database)
        success, results, error = executor.execute_query(db_id=database, sql=sql)

        if success:
            if not results:
                return "Query executed successfully. No rows returned."
            return f"Query executed successfully. Result:\n{results}"
        else:
            return f"Execution Error: {error}"
