## 1. 依赖配置

- [x] 1.1 在 pyproject.toml 中添加 fastapi、uvicorn、slowapi 依赖

## 2. API 实现

- [x] 2.1 创建 `src/api/query.py`，实现 `/query` 端点
- [x] 2.2 创建 `src/main.py`，初始化 FastAPI 应用和限流中间件
- [x] 2.3 在 `src/__init__.py` 中导出 api 路由

## 3. 测试验证

- [x] 3.1 启动 FastAPI 服务验证正常
- [x] 3.2 测试 `/query` 端点返回正确响应（需要 Milvus 服务运行）
- [x] 3.3 测试限流功能（1分钟超过10次返回429）
