"""
测试 SQL 执行器结果比较功能

验证数值比较时的精度误差容忍特性
"""

import pytest
from graph.sql_executor import SQLExecutor


@pytest.fixture
def sql_executor():
    """SQLExecutor fixture with default tolerance (0.001)"""
    return SQLExecutor()


@pytest.fixture
def sql_executor_strict():
    """SQLExecutor fixture with strict tolerance (0.0)"""
    return SQLExecutor(tolerance=0.0)


class TestValuesEqual:
    """测试 _values_equal 方法"""

    def test_none_values(self, sql_executor):
        """测试 None 值比较"""
        assert sql_executor._values_equal(None, None) is True
        assert sql_executor._values_equal(None, 1) is False
        assert sql_executor._values_equal(1, None) is False

    def test_exact_match(self, sql_executor):
        """测试精确匹配"""
        assert sql_executor._values_equal(1.0, 1.0) is True
        assert sql_executor._values_equal(100, 100) is True
        assert sql_executor._values_equal("hello", "hello") is True

    def test_within_tolerance(self, sql_executor):
        """测试在误差范围内的匹配 (tolerance=0.001)"""
        # 0.001 误差范围内的应该匹配
        assert sql_executor._values_equal(1.0005, 1.0) is True
        assert sql_executor._values_equal(1.0, 1.0005) is True
        assert sql_executor._values_equal(0.001, 0.0) is True
        assert sql_executor._values_equal(-0.001, 0.0) is True

    def test_exceeds_tolerance(self, sql_executor):
        """测试超过误差范围的不匹配"""
        # 超过 0.001 误差范围的应该不匹配
        assert sql_executor._values_equal(1.002, 1.0) is False
        assert sql_executor._values_equal(1.005, 1.0) is False
        assert sql_executor._values_equal(0.002, 0.0) is False

    def test_string_comparison_exact(self, sql_executor):
        """测试字符串精确比较"""
        assert sql_executor._values_equal("1.0", "1.0") is True
        # "1.0" 和 "1" 在数值上是相等的（差值为0），所以会匹配
        assert sql_executor._values_equal("1.0", "1") is True
        assert sql_executor._values_equal("hello", "world") is False
        assert sql_executor._values_equal("abc", "123") is False  # 非数值字符串

    def test_int_vs_float(self, sql_executor):
        """测试整数与浮点数比较"""
        assert sql_executor._values_equal(1, 1.0) is True
        assert sql_executor._values_equal(100, 100.0) is True

    def test_negative_numbers(self, sql_executor):
        """测试负数比较"""
        assert sql_executor._values_equal(-1.0005, -1.0) is True
        assert sql_executor._values_equal(-1.002, -1.0) is False
        assert sql_executor._values_equal(-0.5, 0.5) is False


class TestCompareResults:
    """测试 _compare_results 方法"""

    def test_empty_results(self, sql_executor):
        """测试空结果比较"""
        assert sql_executor._compare_results([], []) is True
        assert sql_executor._compare_results(None, None) is True

    def test_different_row_count(self, sql_executor):
        """测试不同行数"""
        result1 = [{"a": 1}, {"a": 2}]
        result2 = [{"a": 1}]
        assert sql_executor._compare_results(result1, result2) is False

    def test_exact_match(self, sql_executor):
        """测试精确匹配"""
        result1 = [{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]
        result2 = [{"col1": 1, "col2": "a"}, {"col1": 2, "col2": "b"}]
        assert sql_executor._compare_results(result1, result2) is True

    def test_within_tolerance(self, sql_executor):
        """测试在误差范围内的匹配"""
        result1 = [{"value": 1.0005}]
        result2 = [{"value": 1.0}]
        assert sql_executor._compare_results(result1, result2) is True

    def test_exceeds_tolerance(self, sql_executor):
        """测试超过误差范围的不匹配"""
        result1 = [{"value": 1.005}]
        result2 = [{"value": 1.0}]
        assert sql_executor._compare_results(result1, result2) is False

    def test_row_order_different(self, sql_executor):
        """测试行顺序不同的情况"""
        result1 = [{"a": 2}, {"a": 1}]
        result2 = [{"a": 1}, {"a": 2}]
        assert sql_executor._compare_results(result1, result2) is True

    def test_subset_columns(self, sql_executor):
        """测试生成结果包含额外列的情况"""
        # result1 有额外列，应该匹配
        result1 = [{"a": 1, "extra": 100}]
        result2 = [{"a": 1}]
        assert sql_executor._compare_results(result1, result2) is True

    def test_multiple_rows_within_tolerance(self, sql_executor):
        """测试多行都在误差范围内"""
        result1 = [
            {"value": 1.0005},
            {"value": 2.0003},
            {"value": 3.0009}
        ]
        result2 = [
            {"value": 1.0},
            {"value": 2.0},
            {"value": 3.0}
        ]
        assert sql_executor._compare_results(result1, result2) is True


class TestStrictTolerance:
    """测试严格 tolerance=0.0 的情况"""

    def test_strict_exact_match(self, sql_executor_strict):
        """测试严格模式下的精确匹配"""
        assert sql_executor_strict._values_equal(1.0, 1.0) is True
        assert sql_executor_strict._values_equal(1, 1.0) is True

    def test_strict_small_difference(self, sql_executor_strict):
        """测试严格模式下即使很小的差异也不匹配"""
        assert sql_executor_strict._values_equal(1.0005, 1.0) is False
        assert sql_executor_strict._values_equal(0.0001, 0.0) is False


class TestCustomTolerance:
    """测试自定义 tolerance"""

    def test_custom_tolerance_0_01(self):
        """测试自定义 tolerance=0.01"""
        executor = SQLExecutor(tolerance=0.01)
        assert executor._values_equal(1.005, 1.0) is True  # 0.005 < 0.01
        assert executor._values_equal(1.02, 1.0) is False  # 0.02 > 0.01
