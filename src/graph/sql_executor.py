"""
SQL 执行器模块

负责连接 MySQL 数据库并执行 SQL 查询。
"""

import logging
from typing import Any

import pymysql
from pymysql.cursors import DictCursor

from config import PROJECT_LOGGER_NAME

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


class SQLExecutor:
    """SQL 执行器（MySQL）"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 3306,
        user: str = "root",
        password: str = "123",
        database: str = "bird",
        timeout: int = 10,  # SQL 执行超时（秒）
        tolerance: float = 0.001  # 数值比较误差容忍度
    ):
        """
        初始化 SQL 执行器

        Args:
            host: MySQL 主机地址
            port: MySQL 端口
            user: 用户名
            password: 密码
            database: 数据库名
            timeout: SQL 执行超时时间（秒），默认10秒
            tolerance: 数值比较误差容忍度，默认 0.001
        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._timeout = timeout
        self._tolerance = tolerance

    def _get_connection(self) -> pymysql.Connection:
        """获取数据库连接"""
        return pymysql.connect(
            host=self._host,
            port=self._port,
            user=self._user,
            password=self._password,
            database=self._database,
            charset='utf8mb4',
            cursorclass=DictCursor,
            read_timeout=self._timeout,
            write_timeout=self._timeout
        )

    def execute_query(
        self,
        db_id: str,
        sql: str,
        max_rows: int = 1000
    ) -> tuple[bool, list[dict[str, Any]], str]:
        """
        执行查询 SQL 并返回结果

        Args:
            db_id: 数据库 ID（用于日志记录）
            sql: SQL 查询语句
            max_rows: 最大返回行数

        Returns:
            (是否成功, 结果列表)
        """
        # 去除代码块标记
        clean_sql = self._remove_code_blocks(sql)

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # 执行查询
            cursor.execute(clean_sql)
            rows = cursor.fetchmany(max_rows)

            # 转换为字典列表
            results = []
            for row in rows:
                results.append({key: row[key] for key in row.keys()})

            cursor.close()
            conn.close()
            return True, results, ""

        except pymysql.Error as e:
            error_code = e.args[0] if e.args else None
            error_msg = str(e)
            # 超时错误 (2006=连接超时, 2013=连接关闭, 其他超时错误)
            if error_code in (2006, 2013, 3024) or 'timed out' in str(e).lower():
                logger.error(f"[SQLExecutor] SQL 执行超时 (>{self._timeout}秒) ({db_id}): {sql}")
            else:
                logger.error(f"[SQLExecutor] SQL 执行失败 ({db_id}): {e}")
            return False, [], error_msg
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[SQLExecutor] 未知错误 ({db_id}): {e}")
            return False, [], error_msg

    def _remove_code_blocks(self, sql: str) -> str:
        """去除 SQL 代码块标记"""
        import re
        pattern = r"```sql?\s*|\s*```"
        return re.sub(pattern, "", sql, flags=re.IGNORECASE).strip()

    def _values_equal(self, val1: Any, val2: Any, tolerance: float | None = None) -> bool:
        """
        比较两个值是否相等（支持数值精度误差容忍）

        如果两个值都可以转换为数值，则使用误差容忍比较。
        否则使用精确比较。

        Args:
            val1: 第一个值
            val2: 第二个值
            tolerance: 误差容忍度，默认使用 self._tolerance

        Returns:
            是否相等
        """
        if tolerance is None:
            tolerance = self._tolerance

        # 处理 None
        if val1 is None and val2 is None:
            return True
        if val1 is None or val2 is None:
            return False

        # 尝试转换为数值比较
        try:
            num1 = float(val1)
            num2 = float(val2)
            return abs(num1 - num2) <= tolerance
        except (ValueError, TypeError):
            # 非数值类型（字符串等），使用精确比较
            return val1 == val2

    def _compare_results(
        self,
        result1: list[dict[str, Any]],
        result2: list[dict[str, Any]]
    ) -> bool:
        """
        比较两个查询结果是否一致（支持超集匹配）

        如果 result1 的列是 result2 列的超集，且所有公共列的值都匹配，则视为匹配。
        这允许生成SQL返回比预期更多的列。

        Args:
            result1: 第一个查询结果（生成的结果）
            result2: 第二个查询结果（预期的结果）

        Returns:
            结果是否匹配
        """
        # 如果两个都为空，认为匹配
        if not result1 and not result2:
            return True

        # 如果数量不同，不匹配
        if len(result1) != len(result2):
            return False

        try:
            return self._values_match_with_subset(result1, result2)
        except Exception as e:
            logger.warning(f"[SQLExecutor] 结果比较失败: {e}")
            return False

    def _values_match_with_subset(self, result1: list[dict], result2: list[dict]) -> bool:
        """
        比较结果，忽略列名，生成结果的值可以是预期结果的超集

        规则：
        1. 行数必须相同
        2. 预期结果和生成结果的行可以任意顺序对应
        3. 生成结果的每行值集合必须包含对应预期行值集合
        4. 数值比较支持误差容忍（self._tolerance）

        Args:
            result1: 生成的结果（可以有额外列）
            result2: 预期的结果

        Returns:
            是否匹配
        """
        # 类型检查：确保是字典列表
        if not isinstance(result1, list) or not isinstance(result2, list):
            return False

        # 确保每个元素都是字典
        for row in result1:
            if not isinstance(row, dict):
                return False
        for row in result2:
            if not isinstance(row, dict):
                return False

        if len(result1) != len(result2):
            return False

        n = len(result1)
        if n == 0:
            return True

        # 预处理：提取每个值的数值类型（用于误差容忍比较）
        # 对于每个值，存储 (原始值, 数值) 元组
        def get_value_info(val):
            try:
                return (val, float(val))
            except (ValueError, TypeError):
                return (val, None)

        result1_values = [[get_value_info(v) for v in row.values()] for row in result1]
        result2_values = [[get_value_info(v) for v in row.values()] for row in result2]

        # 每个位置的使用次数限制
        pos_usage_in_result1 = {i: 0 for i in range(n)}

        # 按预期结果行遍历，检查每行的值都能在生成结果中找到
        for i, row2_values in enumerate(result2_values):
            matched = False

            # 尝试在生成结果中找到匹配的行
            for j, row1_values in enumerate(result1_values):
                # 检查 row2 的所有值是否都能在 row1 中找到匹配
                all_values_matched = True
                for val2_orig, val2_num in row2_values:
                    value_found = False
                    for val1_orig, val1_num in row1_values:
                        # 使用 _values_equal 进行比较
                        if self._values_equal(val1_orig, val2_orig):
                            value_found = True
                            break
                    if not value_found:
                        all_values_matched = False
                        break

                if all_values_matched:
                    # 检查这个位置还能否被使用（防止过度复用）
                    # 一个位置最多被使用其值数量相同的次数
                    max_usage = len(result1[j].values())
                    if pos_usage_in_result1[j] < max_usage:
                        pos_usage_in_result1[j] += 1
                        matched = True
                        break

            if not matched:
                return False

        return True

    def check_connection(self) -> bool:
        """检查数据库连接是否正常"""
        try:
            conn = self._get_connection()
            conn.ping(reconnect=True)
            conn.close()
            return True
        except Exception as e:
            logger.warning(f"[SQLExecutor] 数据库连接失败: {e}")
            return False
