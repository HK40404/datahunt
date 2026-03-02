## ADDED Requirements

### Requirement: Query API Endpoint
系统 SHALL 提供 POST `/query` 端点，接受用户请求并返回 SQL 执行结果。

#### Scenario: Successful query
- **WHEN** 客户端发送 POST `/query` 请求，包含有效的 messages 列表
- **THEN** 系统返回 JSON 响应，包含 `exec_result` 和 `generated_sql` 字段

#### Scenario: Request with optional fields
- **WHEN** 客户端发送请求时包含 `evidence` 和 `database` 可选字段
- **THEN** 系统使用提供的值进行查询

#### Scenario: Rate limiting
- **WHEN** 客户端在 1 分钟内发送超过 10 次请求
- **THEN** 系统返回 429 Too Many Requests 错误

### Requirement: Request Validation
系统 SHALL 验证请求参数的合法性。

#### Scenario: Valid message format
- **WHEN** 请求中 messages 包含 `role` 和 `content` 字段
- **THEN** 系统接受请求并处理

#### Scenario: Invalid message format
- **WHEN** 请求中 messages 缺少必需字段
- **THEN** 系统返回 422 Unprocessable Entity 错误

### Requirement: Error Handling
系统 SHALL 处理查询过程中的错误并返回有意义的错误信息。

#### Scenario: SQL execution error
- **WHEN** 生成的 SQL 执行失败
- **THEN** 响应中 `exec_result` 为空，`exec_error` 包含错误信息

#### Scenario: Validation error
- **WHEN** 生成的 SQL 通过验证失败
- **THEN** 响应中 `validate_error` 包含验证错误信息
