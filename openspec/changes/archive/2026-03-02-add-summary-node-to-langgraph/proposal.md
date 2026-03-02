## Why

当前 LangGraph 应用在 SQL 执行完成后直接返回结果，用户看到的是原始 SQL 和执行结果，缺少一个统一的总结节点来生成面向用户的自然语言答案。当 SQL 执行出错时，也没有友好的错误提示。

## What Changes

- 在 LangGraph 工作流的末尾增加一个 `summary` 节点
- `summary` 节点接收：问题（question）、生成的 SQL（generated_sql）、执行结果（exec_result）或错误信息
- 根据以上信息生成自然语言答案写入 `answer` 字段
- 当前置节点出错时，生成友好的错误提示

## Capabilities

### New Capabilities

- `sql-result-summary`: 新增总结节点，根据 SQL 查询结果生成自然语言答案

### Modified Capabilities

- 无

## Impact

- 新增文件：`src/graph/summary.py`（summary 节点实现）
- 修改文件：`src/graph/graph.py`（添加 summary 节点到工作流）
- 修改文件：`src/graph/state.py`（添加 answer 字段到 State）
