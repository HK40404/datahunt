"""
Pytest 共享 Fixtures

提供项目通用的测试 fixtures：
- Mock LLM 客户端
- Mock Milvus 客户端
- 样本数据 fixtures
"""

import os
from typing import Any

import pytest
from dotenv import load_dotenv

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from data_types.message import Message, RoleType
from llm.llm_base import LLMClientBase, LLMConfig
from llm.openai import OpenAIClient

# 加载环境变量
load_dotenv(dotenv_path="config/.env")


# ========== Mock LLM 客户端 ==========


class MockLLMClient(LLMClientBase):
    """Mock LLM 客户端，用于测试"""

    def __init__(self, response_text: str = "mock response"):
        config = LLMConfig(api_key="mock-key", model="mock-model")
        super().__init__(config)
        self.response_text = response_text
        self.chat_calls = []
        self.chat_structured_output_calls = []

    def initialize_client(self):
        """Mock 初始化，不需要真实客户端"""
        pass

    async def chat(self, messages, **kwargs):
        """Mock chat 方法"""
        self.chat_calls.append({"messages": messages, "kwargs": kwargs})
        return type("MockResponse", (), {"content": self.response_text})()

    async def chat_structured_output(self, messages, *, response_format, **kwargs):
        """Mock chat_structured_output 方法，记录调用参数"""
        self.chat_structured_output_calls.append({
            "messages": messages,
            "response_format": response_format,
            "kwargs": kwargs
        })

        # 尝试返回 response_format 的实例
        if hasattr(response_format, "model_fields"):
            # Pydantic 模型
            return response_format(**{f: "" for f in response_format.model_fields})
        return None

    @staticmethod
    def build_tool_schema(tools):
        """Mock build_tool_schema 方法"""
        return []


class MockOpenAIClient(OpenAIClient):
    """Mock OpenAI 客户端，用于测试"""

    def __init__(self, response_text: str = "mock response"):
        # 使用真实配置但 mock 客户端
        super().__init__(config=DATAHUNT_CONFIG.openai)
        self.response_text = response_text

    async def chat(self, messages, **kwargs):
        self.chat_calls.append({"messages": messages, "kwargs": kwargs})
        return type("MockResponse", (), {"content": self.response_text})()

    async def chat_structured_output(self, messages, *, response_format, **kwargs):
        self.chat_structured_output_calls.append({
            "messages": messages,
            "response_format": response_format,
            "kwargs": kwargs
        })

        if hasattr(response_format, "model_fields"):
            return response_format(**{f: "" for f in response_format.model_fields})
        return None


# ========== Fixtures ==========


@pytest.fixture
def mock_llm_client():
    """创建 Mock LLM 客户端"""
    return MockLLMClient()


@pytest.fixture
def mock_openai_client():
    """创建 Mock OpenAI 客户端"""
    return MockOpenAIClient()


@pytest.fixture
def sample_messages():
    """创建样本对话消息"""
    return [
        Message(role=RoleType.USER, content="查询销售额"),
        Message(role=RoleType.ASSISTANT, content="您想查询哪个时间段的销售额？"),
        Message(role=RoleType.USER, content="2023年的"),
    ]


@pytest.fixture
def sample_state():
    """创建样本 LangGraph State"""
    return {
        "question": "查询2023年销售额",
        "messages": [],
        "evidence": "",
        "database": "test_db",
        "matched_tables": ["sales"],
        "DDL": ["Table: sales (id INT, amount DECIMAL, date DATE)"],
        "generated_sql": "SELECT * FROM sales",
        "exec_result": [],
        "exec_error": "",
        "validate_error": "",
        "review_result": True,
        "review_comment": "",
    }


@pytest.fixture
def sample_ddl():
    """创建样本 DDL"""
    return [
        "Table: customers (CustomerID INT, Name VARCHAR(100), Email VARCHAR(200))",
        "Table: orders (OrderID INT, CustomerID INT, OrderDate DATE, TotalAmount DECIMAL)",
    ]


@pytest.fixture
def sample_schema_result():
    """创建样本 Schema Linking 结果"""
    return {
        "tables": ["customers", "orders"],
        "DDL": [
            "Table: customers\nColumns:\n- CustomerID: INT\n- Name: VARCHAR(100)\n- Email: VARCHAR(200)",
            "Table: orders\nColumns:\n- OrderID: INT\n- CustomerID: INT\n- OrderDate: DATE\n- TotalAmount: DECIMAL"
        ],
        "score": 0.95,
        "reason": "customers 和 orders 表通过 CustomerID 关联，直接匹配查询需求"
    }


# ========== Database Fixtures (Conditional) ==========


@pytest.fixture
def milvus_client():
    """创建 Milvus 客户端（如果可用）"""
    try:
        from vectordb.milvus import MilvusWrapper
        client = MilvusWrapper()
        yield client
    except Exception as e:
        pytest.skip(f"Milvus 不可用: {e}")


# ========== Utility Fixtures ==========


@pytest.fixture
def temp_dir(tmp_path):
    """提供临时目录"""
    return tmp_path


@pytest.fixture
def check_openai_api_key():
    """检查 OpenAI API Key 是否设置"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY 环境变量未设置，跳过测试")
    return api_key


@pytest.fixture
def check_gemini_api_key():
    """检查 Gemini API Key 是否设置"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY 环境变量未设置，跳过测试")
    return api_key
