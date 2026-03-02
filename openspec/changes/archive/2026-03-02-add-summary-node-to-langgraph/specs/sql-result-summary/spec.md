## ADDED Requirements

### Requirement: Summary 节点生成自然语言答案
Summary 节点 SHALL 接收问题（question）、生成的 SQL（generated_sql）和执行结果（exec_result），生成面向用户的自然语言答案并写入 answer 字段。

#### Scenario: SQL 执行成功时生成答案
- **WHEN** SQL 执行完成且 exec_result 包含有效数据
- **THEN** summary 节点生成自然语言答案，准确反映查询结果

#### Scenario: SQL 执行成功但无返回数据
- **WHEN** SQL 执行完成但 exec_result 为空
- **THEN** summary 节点生成"未找到相关数据"的答案

### Requirement: 错误场景生成统一提示
当前置节点出现错误时，summary 节点 SHALL 生成统一的错误提示。

#### Scenario: 查询失败
- **WHEN** 存在 validate_error 或 exec_error
- **THEN** summary 节点生成统一的错误提示，告知用户查询失败
