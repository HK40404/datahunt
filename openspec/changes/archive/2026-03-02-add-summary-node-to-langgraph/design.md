## Context

当前 LangGraph 工作流在 SQL 执行完成后结束，返回的是原始的 SQL 和执行结果。用户在最终输出中看到的是结构化的数据而非面向用户的自然语言答案。当 SQL 执行出错时（如语法错误、执行超时），用户只能看到错误信息，缺乏友好的错误提示。

## Goals / Non-Goals

**Goals:**
- 在工作流末尾增加 summary 节点，生成面向用户的自然语言答案
- 区分成功和失败场景，提供不同的输出格式
- 不修改现有节点的逻辑

**Non-Goals:**
- 不修改 SQL 生成和验证逻辑
- 不提供多轮对话的总结能力
- 不处理复杂的结果可视化

## Decisions

1. **Summary 节点位置**: 放在 SQL 执行节点之后，作为最后一个节点
2. **Answer 字段**: 新增 `answer` 字段到 LangGraph State，用于存储最终答案
3. **错误处理**: 使用 State 中的 `validate_error` 或 `exec_error` 判断是否出错

## Risks / Trade-offs

- [Risk] LLM 生成的回答可能不够准确 → [Mitigation] 使用结构化 prompt 要求 LLM 严格按照结果生成答案
- [Risk] 执行结果为空时如何生成答案 → [Mitigation] 在 prompt 中明确处理空结果的情况
