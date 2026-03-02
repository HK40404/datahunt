"""
测试 SQLAgent 的 SQL 修复功能（fix 模式）

测试用例基于评估结果中的语义理解错误案例设计（result mismatch）
"""

import pytest

from agent.agent.sql_agent import SQLAgent, SQLAgentState


@pytest.fixture
def agent():
    """SQLAgent fixture"""
    return SQLAgent(max_execute_count=5)


@pytest.mark.asyncio
async def test_column_name_typo(agent):
    """
    测试语义理解错误修复：列名拼写错误

    原始 SQL 使用了不存在的列名（如 Region 应为 A2），导致结果不正确。
    """
    state = SQLAgentState(
        question="What region is customer 5 located in?",
        evidence="district 表有 A2 列表示区域名称",
        DDL=[
            "Table: district\nColumns:\n- district_id: INT\n- A2: VARCHAR(50)"
        ],
        original_sql="SELECT Region FROM district WHERE district_id = 5",
        validate_error="Unknown column 'Region' in 'field list'",
        execution_result=[],
        database="bird"
    )

    result = await agent.run(state)

    # 修复后的 SQL 应使用正确的列名 A2
    assert "A2" in result, \
        f"修复后的 SQL 应使用正确的列名 A2，实际结果: {result}"


@pytest.mark.asyncio
async def test_column_alias_error(agent):
    """
    测试语义理解错误修复：列别名使用错误

    ID: 1481 变体 - 问题要求计算两种货币的平均消费差值，
    但 SQL 使用了错误的列别名导致结果不正确。
    """
    state = SQLAgentState(
        question="What is the difference in the annual average consumption of gas between customers who paid in CZK and customers who paid in EUR in 2013?",
        evidence="customers 表有 Currency 列，yearmonth 表有 Consumption",
        DDL=[
            "Table: customers\nColumns:\n- CustomerID: INT\n- Currency: VARCHAR(10)",
            "Table: yearmonth\nColumns:\n- CustomerID: INT\n- Date: VARCHAR(10)\n- Consumption: DECIMAL"
        ],
        original_sql="SELECT AVG(consumption) - AVG(consumption) FROM customers c JOIN yearmonth y ON c.CustomerID = y.CustomerID WHERE c.Currency IN ('CZK', 'EUR') AND SUBSTRING(y.Date, 1, 4) = '2013'",
        validate_error="Unknown column 'consumption' in 'field list'",
        execution_result=[],
        database="bird"
    )

    result = await agent.run(state)

    # 修复后的 SQL 应使用正确的列名 Consumption（大写）
    assert "Consumption" in result, \
        f"修复后的 SQL 应使用正确的列名 Consumption，实际结果: {result}"


@pytest.mark.asyncio
async def test_conditional_aggregation_error(agent):
    """
    测试语义理解错误修复：条件聚合逻辑错误

    ID: 1482 变体 - 问题要求比较三个 segment 的消费，
    但 SQL 使用了复杂的 CASE WHEN 且结果不正确。
    """
    state = SQLAgentState(
        question="Which of the three segments—SME, LAM and KAM—has the biggest consumption?",
        evidence="customers 表有 Segment 列，yearmonth 表有 Consumption",
        DDL=[
            "Table: customers\nColumns:\n- CustomerID: INT\n- Segment: VARCHAR(20)",
            "Table: yearmonth\nColumns:\n- CustomerID: INT\n- Consumption: DECIMAL"
        ],
        original_sql="SELECT T1.Segment, SUM(CASE WHEN T2.Date IS NOT NULL THEN T2.Consumption ELSE 0 END) FROM customers T1 LEFT JOIN yearmonth T2 ON T1.CustomerID = T2.CustomerID WHERE T1.Segment IN ('SME', 'LAM', 'KAM')",
        validate_error="",
        execution_result=[],  # 执行成功但结果错误
        database="bird"
    )

    result = await agent.run(state)

    # 修复后的 SQL 应正确计算三个 segment 的消费比较
    # 验证要点：GROUP BY 和 ORDER BY LIMIT 1 用于找出最大值
    assert "GROUP BY" in result.upper(), \
        f"修复后的 SQL 应使用 GROUP BY 聚合，实际结果: {result}"
    assert "ORDER BY" in result.upper() and "LIMIT" in result.upper(), \
        f"修复后的 SQL 应使用 ORDER BY 和 LIMIT 1 获取最大值，实际结果: {result}"
