---
title: 在 LangGraph 应用中添加 Summary 节点生成自然语言答案
date: 2026-03-03
type: feature-request
status: completed
components:
  - src/graph/graph.py
  - src/graph/summary.py
  - src/api/query.py
  - config/prompt.yaml
category: integration-issues
tags:
  - langgraph
  - summary-node
  - natural-language-answer
  - sql-query
---

# 在 LangGraph 应用中添加 Summary 节点生成自然语言答案

## 问题描述

当前 LangGraph 应用在 SQL 执行完成后直接返回原始结果给用户，用户看到的是结构化的 SQL 和执行结果，缺乏面向用户的自然语言答案。当 SQL 执行出错时，用户只能看到错误信息，缺乏友好的错误提示。

## 解决方案概述

在 LangGraph 工作流的末尾增加一个 `summary` 节点，根据 SQL 查询结果生成面向用户的自然语言答案。

### 核心功能

1. **成功场景**：SQL 执行成功后，根据 question、generated_sql、exec_result 生成自然语言答案
2. **空结果场景**：exec_result 为空时，返回"未找到相关数据"
3. **错误场景**：存在 validate_error 或 exec_error 时，返回统一的错误提示"查询错误达最大次数，请稍后重试"

## 实现细节

### 1. 新增 State 字段

在 `src/graph/graph.py` 中添加 `answer` 字段：

```python
class State(TypedDict):
    # ... 其他字段 ...
    answer: str | None  # 最终答案（summary 节点生成）
```

### 2. 创建 Summary 节点模块

创建 `src/graph/summary.py`：

```python
class SummaryNode:
    """Summary 节点：根据查询结果生成自然语言答案"""

    def __init__(self, llm_client: LLMClientBase = sql_generator_client):
        self._llm = llm_client
        self._prompt_config = DATAHUNT_CONFIG.PROMPT.sql_summary
        self._system_prompt = self._prompt_config.system
        self._user_template = self._prompt_config.user

    async def generate(
        self,
        question: str,
        generated_sql: str,
        exec_result: list[dict[str, Any]],
        validate_error: str | None,
        exec_error: str,
    ) -> str:
        # 错误场景
        if validate_error or exec_error:
            return "查询错误达最大次数，请稍后重试。"

        # 空结果场景
        if not exec_result:
            return "未找到相关数据。"

        # 成功场景：调用 LLM 生成答案
        user_prompt = self._build_user_prompt(question, generated_sql, exec_result)
        messages = [Message.system_message(self._system_prompt), Message.user_message(user_prompt)]
        response = await self._llm.chat([m.to_dict() for m in messages])
        return response.content if hasattr(response, "content") else str(response)
```

### 3. 工作流集成

在 `src/graph/graph.py` 中添加 summary 节点和条件边：

```python
# 添加节点
graph.add_node("summary", self.summarize)

# 条件边：sql_execute 成功 → summary，失败 → sql_fix
graph.add_conditional_edges(
    "sql_execute",
    self._should_execute_fail,
    {"sql_fix": "sql_fix", "summary": "summary"}
)

# summary 节点直接结束
graph.add_edge("summary", END)

# 修复完成判断：fix_count 达上限 → summary
def _should_fix_complete(self, state: State) -> str:
    fix_count = state.get("fix_count", 0)
    if fix_count >= self.MAX_FIX_COUNT:
        return "summary"
    return "validate"
```

### 4. API 响应扩展

在 `src/api/query.py` 中添加 `answer` 字段到响应：

```python
class QueryResponse(BaseModel):
    exec_result: list[dict[str, Any]]
    generated_sql: str
    answer: str | None = Field(default=None, description="自然语言答案")
```

### 5. Prompt 配置

在 `config/prompt.yaml` 中添加：

```yaml
sql_summary:
  system: |
    你是一个数据分析助手，负责根据 SQL 查询结果生成面向用户的自然语言答案。

    要求：
    1. 直接回答用户问题，不需要提及 SQL 或数据库实现细节
    2. 如果查询结果为空，告知用户未找到相关数据
    3. 答案要简洁、准确、易于理解

  user: |
    问题：{question}

    生成的SQL：{generated_sql}

    查询结果：{exec_result}

    请根据以上信息生成面向用户的自然语言答案。
```

## 工作流节点流程

```
START → query_rewrite → schema_link → sql_generator → sql_validator
                                    ↓
                              [验证失败] → sql_fix → sql_validator
                                    ↓
                              [验证成功] → sql_execute
                                    ↓
                     [执行失败/空结果] → sql_fix → sql_validator
                                    ↓
                              [执行成功] → summary → END
```

## 测试结果

| 问题 | 生成的 SQL | Answer |
|------|-----------|--------|
| What is the ratio of customers who pay in EUR against customers who pay in CZK? | SELECT CAST(SUM(CASE WHEN Currency = 'EUR' THEN 1 ELSE 0 END)... | 支付欧元的客户与支付捷克克朗的客户比例约为 0.066（即大约 1:15） |
| In 2012, who had the least consumption in LAM? | SELECT T1.CustomerID FROM customers... | 在2012年，LAM客户中消费最少的是客户ID为47273的客户 |

## 预防策略

### 添加新节点到 LangGraph 前的检查清单

1. **State 字段设计**：
   - 确认新字段的必要性
   - 确定字段类型（使用 `str | None` 等确保兼容性）
   - 评估字段流动性：哪些节点需要读写该字段？

2. **节点模块化**：
   - 独立模块文件（如 summary.py）
   - 清晰的文档字符串
   - 全局实例导出

3. **条件边设计**：
   - 使用有意义的函数命名（如 `_should_execute_fail`）
   - 条件边映射清晰（节点名: 目标节点）
   - 处理成功/失败多条路径

4. **错误处理模式**：
   - 先处理错误场景
   - 再处理空数据场景
   - 最后处理正常场景

### 测试用例建议

```python
# 成功场景测试
@pytest.mark.asyncio
async def test_generate_success_with_data():
    node = SummaryNode(llm_client=mock_llm)
    result = await node.generate(
        question="本月销售额是多少？",
        generated_sql="SELECT SUM(amount) FROM sales",
        exec_result=[{"sum": 10000}],
        validate_error=None,
        exec_error=""
    )
    assert result is not None
    mock_llm.chat.assert_called_once()

# 错误场景测试
@pytest.mark.asyncio
async def test_generate_with_error():
    node = SummaryNode(llm_client=mock_llm)
    result = await node.generate(
        question="test",
        generated_sql="test",
        exec_result=[],
        validate_error="SQL语法错误",
        exec_error=""
    )
    assert result == "查询错误达最大次数，请稍后重试。"
```

## 相关文档

- [openspec/specs/sql-result-summary/spec.md](../../openspec/specs/sql-result-summary/spec.md) - 功能规格文档
- [openspec/changes/archive/2026-03-02-add-summary-node-to-langgraph/](../../openspec/changes/archive/2026-03-02-add-summary-node-to-langgraph/) - 变更归档

## 相关代码文件

- `src/graph/graph.py` - LangGraph 工作流定义
- `src/graph/summary.py` - Summary 节点实现
- `src/api/query.py` - API 端点
- `config/prompt.yaml` - Prompt 配置
