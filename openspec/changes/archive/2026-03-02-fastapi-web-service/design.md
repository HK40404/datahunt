## Context

当前项目是 LangGraph CLI 应用，仅支持命令行调用。现有架构：
- LangGraph 工作流处理 Text-to-SQL 任务
- 入口函数 `text_to_sql(state)` 返回完整 State
- 使用 pydantic-settings + YAML 配置管理

需要将其改造为 FastAPI Web 应用，提供 HTTP API 接口。

## Goals / Non-Goals

**Goals:**
- 新增 FastAPI Web 服务，提供 HTTP API
- 保持现有 LangGraph 逻辑完全不变
- 实现限流功能（每分钟 10 次请求）
- 兼容现有调用方式

**Non-Goals:**
- 不提供流式输出
- 不提供 API 认证
- 不提供多版本 API
- 不持久化会话

## Decisions

### 1. API 路由设计
- **选择**: `/query` 端点（无版本号）
- **理由**: 根据用户需求，去掉版本号简化 URL

### 2. Response 精简
- **选择**: 只返回 `exec_result` 和 `generated_sql`
- **理由**: 用户明确要求简化响应

### 3. 限流方案
- **选择**: slowapi
- **理由**: 用户明确指定，与 FastAPI 集成简单

### 4. 项目结构
- **选择**: `src/main.py` + `src/api/query.py`
- **理由**: 符合用户指定的目录结构

### 5. State 转换
- **选择**: API Request → dict → text_to_sql() → API Response
- **理由**: 最小改动现有代码，直接复用

## Risks / Trade-offs

- **风险**: 现有代码中 `text_to_sql` 是同步调用，但 FastAPI 需要异步
  - **缓解**: 使用 `asyncio.run()` 或将 FastAPI 改为同步函数
- **风险**: 错误处理不统一
  - **缓解**: 在 API 层统一捕获异常，返回标准化错误响应

## Migration Plan

1. 新增依赖: `fastapi`, `uvicorn[standard]`, `slowapi`
2. 创建 `src/api/query.py` 路由
3. 创建 `src/main.py` FastAPI 应用
4. 更新 `pyproject.toml` 添加依赖
5. 测试 API 端点

## Open Questions

(无)
