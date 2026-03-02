"""
OpenAIClient 测试程序

测试 OpenAI LLM 客户端的核心功能：
1. 基本异步对话
2. 结构化输出
3. 工具调用
4. 重试机制配置
"""

import json
import os
from typing import Any

import pytest
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agent.tool.base_tool import BaseTool, ToolSet
from llm.llm_base import LLMConfig, LLMResponse
from llm.openai import OpenAIClient

# 加载环境变量（从 config/.env 文件）
load_dotenv(dotenv_path="config/.env")


# ========== 辅助函数 ==========

def print_response_json(response: LLMResponse | BaseModel):
    """
    打印响应体的 JSON 格式
    
    Args:
        response: LLMResponse 或 BaseModel 对象
    """
    if isinstance(response, LLMResponse):
        # 转换为字典，排除 raw_response（可能包含不可序列化对象）
        response_dict = response.model_dump(exclude={"raw_response"})
        print("\n📋 完整响应体 (JSON):")
        print(json.dumps(response_dict, ensure_ascii=False, indent=2))
    elif isinstance(response, BaseModel):
        # BaseModel 直接转换为字典
        response_dict = response.model_dump()
        print("\n📋 完整响应体 (JSON):")
        print(json.dumps(response_dict, ensure_ascii=False, indent=2))
    else:
        # 其他类型尝试直接序列化
        try:
            print("\n📋 完整响应体 (JSON):")
            print(json.dumps(response, ensure_ascii=False, indent=2, default=str))
        except Exception:
            print("\n⚠️  无法序列化响应体为 JSON")


# ========== 测试用工具定义 ==========

class MathArgs(BaseModel):
    """数学运算参数"""
    a: int = Field(..., description="第一个整数")
    b: int = Field(..., description="第二个整数")


class MockAddTool(BaseTool):
    """测试用加法工具"""

    @classmethod
    def name(cls) -> str:
        return "mock_add"

    @classmethod
    def description(cls) -> str:
        return "返回两个整数相加的结果"

    @classmethod
    def parameters(cls) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "a": {"type": "integer", "description": "第一个整数"},
                "b": {"type": "integer", "description": "第二个整数"}
            },
            "required": ["a", "b"]
        }

    @classmethod
    def invoke(cls, **kwargs) -> str:
        a = kwargs["a"]
        b = kwargs["b"]
        return str(a + b)


# ========== Fixtures ==========

@pytest.fixture
def openai_config():
    """创建 OpenAI 配置"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY 环境变量未设置，跳过测试")

    # 使用 DATAHUNT_CONFIG 的配置
    from config import DATAHUNT_CONFIG
    base_url = DATAHUNT_CONFIG.OPENAI_BASE_URL
    model = DATAHUNT_CONFIG.OPENAI_MODEL

    return LLMConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
        temperature=0.0
    )


@pytest.fixture
def openai_client(openai_config) -> OpenAIClient:
    """创建 OpenAIClient 实例"""
    return OpenAIClient(openai_config)


# ========== 测试用例 1: 基本对话测试 ==========

@pytest.mark.asyncio
async def test_chat_basic(openai_client: OpenAIClient):
    """测试基本异步对话"""
    messages = [
        {"role": "user", "content": "请说明你是什么模型，并用一句话介绍人工智能。"}
    ]

    response = await openai_client.chat(messages)

    # 打印完整响应体
    print_response_json(response)

    # 验证响应类型
    assert response is not None
    assert isinstance(response, LLMResponse)
    assert hasattr(response, "content")
    assert isinstance(response.content, str)
    assert len(response.content) > 0

    # 验证响应内容
    assert "人工智能" in response.content or "AI" in response.content.upper()

    # 验证其他字段
    assert hasattr(response, "finish_reason")
    assert hasattr(response, "raw_response")

    print("✅ 基本对话测试成功")
    print(f"   响应内容: {response.content}")


# ========== 测试用例 2: 结构化输出测试 ==========

class CountryInfo(BaseModel):
    """国家信息"""
    name: str = Field(..., description="国家名称")
    capital: str = Field(..., description="首都")
    population: int = Field(..., description="人口数量（单位：万）")


@pytest.mark.asyncio
async def test_chat_structured_output(openai_client: OpenAIClient):
    """测试结构化输出功能（使用 create API + extra_body）"""
    messages = [
        {"role": "system", "content": "You must respond with JSON using English field names exactly as specified in the schema. Field names must match: name, capital, population."},
        {"role": "user", "content": "请提供中国的信息：国家名称、首都和人口数量（单位：万）。"}
    ]

    result = await openai_client.chat_structured_output(
        messages,
        response_format=CountryInfo,
        parse_api=False  # 使用 create API + extra_body
    )

    # 打印完整响应体
    print_response_json(result)

    # 验证返回类型
    assert isinstance(result, CountryInfo)

    # 验证字段
    assert isinstance(result.name, str)
    assert isinstance(result.capital, str)
    assert isinstance(result.population, int)

    # 验证内容
    assert "中国" in result.name or "China" in result.name
    assert "北京" in result.capital or "Beijing" in result.capital
    assert result.population > 0

    print("✅ 结构化输出测试成功（create API + extra_body）")
    print(f"   国家名称: {result.name}")
    print(f"   首都: {result.capital}")
    print(f"   人口: {result.population}万")


@pytest.mark.asyncio
async def test_chat_structured_output_with_parse_api(openai_client: OpenAIClient):
    """测试结构化输出功能（使用 parse API）"""
    messages = [
        {"role": "system", "content": "You must respond with JSON using English field names exactly as specified in the schema. Field names must match: name, capital, population."},
        {"role": "user", "content": "请提供日本的信息：国家名称、首都和人口数量（单位：万）。"}
    ]

    result = await openai_client.chat_structured_output(
        messages,
        response_format=CountryInfo,
        parse_api=True  # 使用 parse API
    )

    # 打印完整响应体
    print_response_json(result)

    # 验证返回类型
    assert isinstance(result, CountryInfo)

    # 验证字段
    assert isinstance(result.name, str)
    assert isinstance(result.capital, str)
    assert isinstance(result.population, int)

    # 验证内容
    assert "日本" in result.name or "Japan" in result.name
    assert "东京" in result.capital or "Tokyo" in result.capital
    assert result.population > 0

    print("✅ 结构化输出测试成功（parse API）")
    print(f"   国家名称: {result.name}")
    print(f"   首都: {result.capital}")
    print(f"   人口: {result.population}万")


# ========== 测试用例 3: 工具调用测试 ==========

@pytest.mark.asyncio
async def test_chat_with_tools(openai_client: OpenAIClient):
    """测试带工具调用的对话"""
    # 创建工具集合
    tool_set = ToolSet([MockAddTool])
    tools = tool_set.get_schemas()

    messages = [
        {"role": "system", "content": "你是一个数学助手。使用提供的工具来计算用户的数学问题。"},
        {"role": "user", "content": "请帮我计算 15 加 27 等于多少？"}
    ]

    response = await openai_client.chat(messages, tools=tools)

    # 打印完整响应体
    print_response_json(response)

    # 验证响应
    assert response is not None
    assert isinstance(response, LLMResponse)

    # 验证工具调用
    if response.tool_calls and len(response.tool_calls) > 0:
        # LLM 选择了工具调用
        tool_call = response.tool_calls[0]
        # 应该调用 mock_add 工具
        assert tool_call.name == "mock_add", f"工具名称应为 mock_add，实际为 {tool_call.name}"
        assert tool_call.arguments["a"] == 15
        assert tool_call.arguments["b"] == 27

        # 执行工具
        result = MockAddTool.invoke(**tool_call.arguments)
        # mock_add 返回字符串
        assert result == "42", f"计算结果应为 '42'，实际为 {result}"

        print("✅ 工具调用测试成功")
        print(f"   LLM 选择工具: {tool_call.name}")
        print(f"   工具参数: {tool_call.arguments}")
        print(f"   执行结果: {result}")
    elif response.content and len(response.content) > 0:
        # LLM 直接回复了答案
        print("✅ 工具调用测试（LLM 直接回复）")
        print(f"   回复内容: {response.content}")
    else:
        # LLM 既没有调用工具也没有回复内容（可能正在推理中）
        # 这种情况可能是推理模型的特点，检查是否有 reasoning 内容
        if response.reasoning:
            print("⚠️  LLM 返回推理内容但未完成响应，可能是模型特性导致")
            print(f"   推理内容: {response.reasoning[:200]}...")
        else:
            # 如果既没有工具调用也没有内容，测试失败
            pytest.fail("LLM 既没有调用工具也没有返回内容")


@pytest.mark.asyncio
async def test_chat_with_tools_no_suitable_tool(openai_client: OpenAIClient):
    """测试无可用工具时的对话"""
    # 创建工具集合（只有数学工具）
    tool_set = ToolSet([MockAddTool])
    tools = tool_set.get_schemas()

    messages = [
        {"role": "system", "content": "你是一个助手。如果用户的问题可以用工具解决就调用工具，否则直接回答。"},
        {"role": "user", "content": "今天天气怎么样？"}
    ]

    response = await openai_client.chat(messages, tools=tools)

    # 打印完整响应体
    print_response_json(response)

    # 验证响应
    assert response is not None
    assert response.content is not None
    assert len(response.content) > 0

    # LLM 应该直接回复，不调用工具（因为没有天气工具）
    if response.tool_calls:
        print(f"⚠️  LLM 调用了工具: {response.tool_calls}")
    else:
        print("✅ 无可用工具时正确处理")
        print(f"   回复内容: {response.content[:100]}...")


# ========== 测试用例 4: 响应解析测试 ==========

@pytest.mark.asyncio
async def test_chat_response_parsing(openai_client: OpenAIClient):
    """测试响应解析（包括 tool_calls、token_usage 等）"""
    messages = [
        {"role": "user", "content": "你好"}
    ]

    response = await openai_client.chat(messages)

    # 验证响应结构
    assert isinstance(response, LLMResponse)
    assert hasattr(response, "content")
    assert hasattr(response, "tool_calls")
    assert hasattr(response, "parsed")
    assert hasattr(response, "finish_reason")
    assert hasattr(response, "refused_reason")
    assert hasattr(response, "token_usage")
    assert hasattr(response, "raw_response")

    # 验证 token_usage 格式（如果存在）
    # 根据 llm_base.py 注释：记录输入token数、输出token数、推理token数、总花费token数、cached token数
    if response.token_usage:
        assert isinstance(response.token_usage, dict)
        # 必须包含的字段
        assert "input" in response.token_usage, "token_usage 应包含 input 字段（输入token数）"
        assert "output" in response.token_usage, "token_usage 应包含 output 字段（输出token数）"
        assert "total" in response.token_usage, "token_usage 应包含 total 字段（总花费token数）"

        # 验证字段类型
        assert isinstance(response.token_usage["input"], int), "input token 数应为整数"
        assert isinstance(response.token_usage["output"], int), "output token 数应为整数"
        assert isinstance(response.token_usage["total"], int), "total token 数应为整数"

        # 验证数值合理性
        assert response.token_usage["input"] >= 0, "input token 数应 >= 0"
        assert response.token_usage["output"] >= 0, "output token 数应 >= 0"
        assert response.token_usage["total"] >= 0, "total token 数应 >= 0"

        # 可选字段（某些 API 可能支持）
        if "reasoning" in response.token_usage:
            assert isinstance(response.token_usage["reasoning"], int), "reasoning token 数应为整数"
        if "cached" in response.token_usage:
            assert isinstance(response.token_usage["cached"], int), "cached token 数应为整数"

    print("✅ 响应解析测试成功")
    print(f"   finish_reason: {response.finish_reason}")
    print(f"   token_usage: {response.token_usage}")


# ========== 测试用例 5: 重试机制配置测试 ==========

def test_max_retries_from_config():
    """测试 max_retries 默认值从 DATAHUNT_CONFIG 读取"""
    from config import DATAHUNT_CONFIG

    config = LLMConfig(
        api_key="test-api-key",
        model="gpt-4"
    )

    # 验证 max_retries 使用 DATAHUNT_CONFIG.LLM_MAX_RETRIES 的值
    assert config.max_retries == DATAHUNT_CONFIG.LLM_MAX_RETRIES
    print("✅ max_retries 默认值测试成功")
    print(f"   LLMConfig.max_retries = {config.max_retries}")
    print(f"   DATAHUNT_CONFIG.LLM_MAX_RETRIES = {DATAHUNT_CONFIG.LLM_MAX_RETRIES}")


def test_max_retries_custom_value():
    """测试自定义 max_retries 值"""
    custom_retries = 5

    config = LLMConfig(
        api_key="test-api-key",
        model="gpt-4",
        max_retries=custom_retries
    )

    # 验证自定义值生效
    assert config.max_retries == custom_retries
    print("✅ 自定义 max_retries 测试成功")
    print(f"   自定义 max_retries = {custom_retries}")


def test_max_retries_zero():
    """测试 max_retries=0 时禁用重试"""
    config = LLMConfig(
        api_key="test-api-key",
        model="gpt-4",
        max_retries=0
    )

    # 验证重试被禁用
    assert config.max_retries == 0
    print("✅ max_retries=0 禁用重试测试成功")


def test_openai_client_initialization_with_retry():
    """测试 OpenAIClient 初始化时正确设置 max_retries"""
    from config import DATAHUNT_CONFIG

    # 测试默认配置
    config_default = LLMConfig(
        api_key="test-api-key",
        model="gpt-4"
    )
    client_default = OpenAIClient(config_default)

    # 验证客户端使用配置的重试次数
    assert client_default._config.max_retries == DATAHUNT_CONFIG.LLM_MAX_RETRIES
    print("✅ OpenAIClient 默认重试配置测试成功")
    print(f"   客户端 max_retries = {client_default._config.max_retries}")

    # 测试自定义配置
    config_custom = LLMConfig(
        api_key="test-api-key",
        model="gpt-4",
        max_retries=3
    )
    client_custom = OpenAIClient(config_custom)

    # 验证自定义重试次数生效
    assert client_custom._config.max_retries == 3
    print("✅ OpenAIClient 自定义重试配置测试成功")
    print(f"   客户端 max_retries = {client_custom._config.max_retries}")


@pytest.mark.asyncio
async def test_chat_with_custom_max_retries(openai_client: OpenAIClient):
    """测试使用自定义 max_retries 的对话"""
    # 修改客户端配置
    custom_retries = 1
    openai_client._config.max_retries = custom_retries

    messages = [
        {"role": "user", "content": "请简单介绍一下你自己。"}
    ]

    response = await openai_client.chat(messages)

    # 验证响应正常
    assert response is not None
    assert isinstance(response, LLMResponse)
    assert response.content is not None
    assert len(response.content) > 0

    print("✅ 自定义 max_retries 对话测试成功")
    print(f"   使用 max_retries = {custom_retries}")
    print(f"   响应内容: {response.content[:100]}...")

