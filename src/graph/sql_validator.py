"""
SQL 校验器模块

提供 SQL 语法检查和安全性校验功能。
"""

import logging
import re
from typing import TypedDict

import sqlglot

from config import PROJECT_LOGGER_NAME

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

# 禁止的 DDL 关键字
FORBIDDEN_DDL_KEYWORDS = frozenset([
    "DROP", "ALTER", "TRUNCATE", "CREATE", "RENAME", "MODIFY"
])

# 禁止的 DML 关键字（无 WHERE 条件时）
FORBIDDEN_DML_KEYWORDS = frozenset([
    "DELETE", "UPDATE", "INSERT", "REPLACE"
])

# 危险关键字
DANGEROUS_KEYWORDS = frozenset([
    "GRANT", "REVOKE", "EXECUTE", "EXEC", "LOAD_FILE", "INTO OUTFILE",
    "INTO DUMPFILE", "BENCHMARK", "SLEEP", "WAITFOR"
])


class SQLValidationResult(TypedDict):
    """SQL校验结果"""
    is_valid: bool  # 是否通过校验
    error_message: str | None  # 错误信息（如果有）


class SQLValidator:
    """SQL校验器"""

    def __init__(self, database_type: str = "mysql"):
        """
        初始化 SQL 校验器

        Args:
            database_type: 数据库类型（用于 sqlglot 解析），默认 mysql
        """
        self._database_type = database_type

    def validate(self, sql: str) -> SQLValidationResult:
        """
        校验 SQL 语句

        Args:
            sql: 待校验的 SQL 语句

        Returns:
            SQLValidationResult: 校验结果
        """
        if not sql or not sql.strip():
            return SQLValidationResult(
                is_valid=False,
                error_message="SQL 语句为空"
            )

        # 去除 SQL 代码块标记
        clean_sql = self._remove_code_blocks(sql)
        clean_sql = clean_sql.strip()

        # 1. 语法检查
        syntax_result = self._check_syntax(clean_sql)
        if not syntax_result["is_valid"]:
            return syntax_result

        # 2. 安全性检查
        security_result = self._check_security(clean_sql)
        if not security_result["is_valid"]:
            return security_result

        logger.debug(f"[SQLValidator] SQL 校验通过: {clean_sql}")
        return SQLValidationResult(
            is_valid=True,
            error_message=None
        )

    def _remove_code_blocks(self, sql: str) -> str:
        """去除 SQL 代码块标记"""
        # 去除 ```sql 和 ``` 标记
        pattern = r"```sql?\s*|\s*```"
        return re.sub(pattern, "", sql, flags=re.IGNORECASE).strip()

    def _check_syntax(self, sql: str) -> SQLValidationResult:
        """
        检查 SQL 语法

        Args:
            sql: 清洗后的 SQL 语句

        Returns:
            SQLValidationResult: 校验结果
        """
        try:
            # 尝试解析 SQL
            sqlglot.parse(sql, dialect=self._database_type)
            return SQLValidationResult(is_valid=True, error_message=None)
        except Exception as e:
            error_msg = f"SQL 语法错误: {str(e)}"
            logger.warning(f"[SQLValidator] {error_msg}")
            return SQLValidationResult(is_valid=False, error_message=error_msg)

    def _check_security(self, sql: str) -> SQLValidationResult:
        """
        检查 SQL 安全性

        Args:
            sql: 清洗后的 SQL 语句

        Returns:
            SQLValidationResult: 校验结果
        """
        sql_upper = sql.upper()

        # 1. 检查禁止的 DDL
        for keyword in FORBIDDEN_DDL_KEYWORDS:
            # 使用正则匹配完整单词，避免误判
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                error_msg = f"禁止使用 DDL 关键字: {keyword}"
                logger.warning(f"[SQLValidator] {error_msg}")
                return SQLValidationResult(is_valid=False, error_message=error_msg)

        # 2. 检查危险关键字
        for keyword in DANGEROUS_KEYWORDS:
            pattern = r'\b' + keyword + r'\b'
            if re.search(pattern, sql_upper):
                error_msg = f"禁止使用危险关键字: {keyword}"
                logger.warning(f"[SQLValidator] {error_msg}")
                return SQLValidationResult(is_valid=False, error_message=error_msg)

        # 3. 检查 DELETE/UPDATE 是否有 WHERE 条件
        for keyword in FORBIDDEN_DML_KEYWORDS:
            pattern = r'\b' + keyword + r'\b'
            match = re.search(pattern, sql_upper)
            if match:
                # 检查是否有 WHERE 子句
                keyword_pos = match.start()
                remaining_sql = sql_upper[keyword_pos:]

                # 简单检查：是否有关键字后面没有 WHERE
                # 注意：这是一个简化检查，可能会有误判
                if "WHERE" not in remaining_sql:
                    error_msg = f"{keyword} 操作必须包含 WHERE 条件"
                    logger.warning(f"[SQLValidator] {error_msg}")
                    return SQLValidationResult(is_valid=False, error_message=error_msg)

        return SQLValidationResult(is_valid=True, error_message=None)

    def normalize_sql(self, sql: str) -> str:
        """
        规范化 SQL 语句（用于比对）

        Args:
            sql: 原始 SQL 语句

        Returns:
            str: 规范化后的 SQL 语句
        """
        # 去除代码块
        clean_sql = self._remove_code_blocks(sql)
        # 使用 sqlglot 规范化
        try:
            parsed = sqlglot.parseOne(clean_sql, dialect=self._database_type)
            return parsed.sql(dialect=self._database_type)
        except Exception:
            # 如果解析失败，返回清洗后的原始 SQL
            return clean_sql.upper().strip()
