## Why

当前项目是 LangGraph CLI 应用，仅支持命令行调用。需要将其改造为 FastAPI Web 应用，提供 HTTP API 接口，便于其他系统集成和调用。

## What Changes

- 新增 FastAPI 应用入口 (`src/main.py`)
- 新增 API 路由 (`src/api/query.py`)
- 集成 slowapi 限流中间件
- 保持原有 LangGraph 逻辑不变，API 层直接调用

## Capabilities

### New Capabilities
- `query-api`: 提供 `/query` 端点，接受消息列表返回 SQL 执行结果

### Modified Capabilities
(无)

## Impact

- **新增文件**: `src/main.py`, `src/api/query.py`
- **依赖新增**: `fastapi`, `uvicorn`, `slowapi`
- **配置变更**: `pyproject.toml` 新增 API 相关依赖
