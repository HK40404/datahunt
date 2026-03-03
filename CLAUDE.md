# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

DataHunt 是一个基于 LangGraph 的 Text-to-SQL 项目，通过自然语言问题生成并执行 SQL 查询。

## 开发命令

```bash
# 安装依赖（使用 uv）
uv sync

# 运行测试
pytest test/ -vs

# 运行单个测试文件
pytest test/test_openai.py -vs

# 运行带标记的测试
pytest test/test_openai.py -m manual -vs

# 启动 API 服务
python -m uvicorn src.main:app --reload

# 代码检查
ruff check src/ test/
ruff format src/ test/
mypy src/

# pre-commit 钩子
pre-commit install
```

## 项目架构

```
src/
├── main.py                 # FastAPI 入口
├── api/                    # API 路由
├── agent/                  # Agent 实现
├── config/                 # 配置管理
├── context/                # 上下文提供者（Schema、Similar SQL 等）
├── data_types/             # 数据类型定义
├── embed/                  # 向量嵌入模块（BGE、Transformer）
├── graph/                  # LangGraph 流程节点
│   ├── graph.py            # 主流程图定义
│   ├── rewritter.py        # 查询改写
│   ├── sql_generator.py    # SQL 生成
│   ├── sql_validator.py    # SQL 验证
│   ├── sql_executor.py     # SQL 执行
│   ├── sql_fixer.py        # SQL 修复
│   └── reranker.py         # Rerank
├── llm/                    # LLM 客户端（OpenAI、 Gemini）
├── pipeline/                # 基准测试管道
├── tracing/                # 链路追踪
└── vectordb/               # 向量数据库（Milvus、 Chroma）
```

## SQL 生成流程

```
[Query Rewrite] -> [Schema Link] -> [SQL Generate] -> [SQL Validate] -> [SQL Execute]
                                                                  |                 |
                                                                  v                 v
                                                              [SQL Fix] <--------+
                                                                  |
                                                                  +-> [Summary]
```

## 配置

- `config/config.yaml` - 主配置文件
- `config/prompt.yaml` - Prompt 模板
- `config/.env` - 环境变量

## 技术栈

- **图编排**: LangGraph
- **LLM**: OpenAI GPT、 Gemini
- **向量数据库**: Milvus、 ChromaDB
- **向量模型**: BGE、 Sentence-Transformers
- **API**: FastAPI + SlowAPI（限流）
- **测试**: pytest + pytest-asyncio
