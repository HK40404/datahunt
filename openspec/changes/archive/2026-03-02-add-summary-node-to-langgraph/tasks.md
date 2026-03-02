## 1. 准备阶段

- [x] 1.1 查看现有 state.py 结构，确认 LangGraph State 定义位置
- [x] 1.2 查看现有 graph.py 工作流结构，确认节点连接方式

## 2. State 修改

- [x] 2.1 在 LangGraph State 中添加 `answer` 字段（str | None 类型）

## 3. Summary 节点实现

- [x] 3.1 创建 `src/graph/summary.py`，实现 summary 节点
- [x] 3.2 实现成功场景：根据 question、generated_sql、exec_result 生成自然语言答案
- [x] 3.3 实现错误场景：根据 validate_error 或 exec_error 生成统一的错误提示

## 4. 工作流集成

- [x] 4.1 在 graph.py 中添加 summary 节点到工作流（SQL 执行节点之后）
- [x] 4.2 配置 summary 节点的输入输出边

## 5. 测试验证

- [x] 5.1 运行现有测试确保没有破坏现有功能
- [x] 5.2 手动测试 summary 节点输出
