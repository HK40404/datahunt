"""
GeminiClient 测试程序

测试 Gemini LLM 客户端的核心功能：
1. 基本异步对话
2. 结构化输出
3. 工具调用
"""

import json
import os

import pytest
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from agent.tool.tool_manager import ToolManager
from llm.gemini import GeminiClient
from llm.llm_base import LLMConfig, LLMResponse

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


@ToolManager.register_tool(MathArgs)
def mock_add(a: int, b: int) -> str:
    """测试用加法工具"""
    return str(a + b)


# ========== Fixtures ==========

@pytest.fixture
def gemini_config():
    """创建 Gemini 配置"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.skip("GEMINI_API_KEY 环境变量未设置，跳过测试")
    
    return LLMConfig(
        api_key=api_key,
        model=os.getenv("GEMINI_MODEL", "gemini-3-flash-preview"),
        temperature=0.0
    )


@pytest.fixture
def gemini_client(gemini_config) -> GeminiClient:
    """创建 GeminiClient 实例"""
    return GeminiClient(gemini_config)


# ========== 测试用例 1: 基本对话测试 ==========

@pytest.mark.asyncio
async def test_chat_basic(gemini_client: GeminiClient):
    """测试基本异步对话"""
    messages = [
        {"role": "user", "content": "请用一句话介绍人工智能。"}
    ]
    
    response = await gemini_client.chat(messages)
    
    # 打印完整响应体
    print_response_json(response)
    
    # 验证响应类型
    assert response is not None
    assert hasattr(response, "content")
    assert isinstance(response.content, str)
    assert len(response.content) > 0
    
    # 验证响应内容
    assert "人工智能" in response.content or "AI" in response.content.upper()
    
    print("✅ 基本对话测试成功")
    print(f"   响应内容: {response.content}")
    


# ========== 测试用例 2: 结构化输出测试 ==========

class CountryInfo(BaseModel):
    """国家信息"""
    name: str = Field(..., description="国家名称")
    capital: str = Field(..., description="首都")
    population: int = Field(..., description="人口数量（单位：万）")


@pytest.mark.asyncio
async def test_chat_structured_output(gemini_client):
    """测试结构化输出功能"""
    messages = [
        {"role": "user", "content": "请提供中国的信息：国家名称、首都和人口数量（单位：万）。"}
    ]
    
    result = await gemini_client.chat_structured_output(
        messages,
        response_format=CountryInfo
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
    
    print("✅ 结构化输出测试成功")
    print(f"   国家名称: {result.name}")
    print(f"   首都: {result.capital}")
    print(f"   人口: {result.population}万")


@pytest.mark.asyncio
async def test_chat_structured_output_empty_messages(gemini_client):
    """测试结构化输出 - 空消息列表"""
    with pytest.raises(ValueError, match="messages is required"):
        await gemini_client.chat_structured_output(
            [],
            response_format=CountryInfo
        )


# ========== 测试用例 3: 工具调用测试 ==========

@pytest.mark.asyncio
async def test_chat_with_tools(gemini_client):
    """测试带工具调用的对话"""
    # 只获取 mock_add 工具的定义（从测试工具中筛选）
    all_tools = list(ToolManager.default_tools.values())
    mock_add_tool = [tool for tool in all_tools if tool.name == "mock_add"]
    tools = GeminiClient.build_tool_schema(mock_add_tool)
    
    messages = [
        {"role": "system", "content": "你是一个数学助手。使用提供的工具来计算用户的数学问题。"},
        {"role": "user", "content": "请帮我计算 15 加 27 等于多少？"}
    ]
    
    response = await gemini_client.chat(messages, tools=tools)
    
    # 打印完整响应体
    print_response_json(response)
    
    # 验证响应
    assert response is not None
    
    # 验证工具调用
    if response.tool_calls and len(response.tool_calls) > 0:
        # LLM 选择了工具调用
        tool_call = response.tool_calls[0]
        # 应该调用 mock_add 工具
        assert tool_call.name == "mock_add", f"工具名称应为 mock_add，实际为 {tool_call.name}"
        assert tool_call.arguments["a"] == 15
        assert tool_call.arguments["b"] == 27
        
        # 执行工具
        result = ToolManager().call(tool_call.name, tool_call.arguments)
        # mock_add 返回字符串
        assert result == "42", f"计算结果应为 '42'，实际为 {result}"
        
        print("✅ 工具调用测试成功")
        print(f"   LLM 选择工具: {tool_call.name}")
        print(f"   工具参数: {tool_call.arguments}")
        print(f"   执行结果: {result}")
    else:
        # LLM 可能直接回复了答案
        assert response.content is not None
        assert len(response.content) > 0
        print("✅ 工具调用测试（LLM 直接回复）")
        print(f"   回复内容: {response.content}")


@pytest.mark.asyncio
async def test_chat_with_tools_no_suitable_tool(gemini_client):
    """测试无可用工具时的对话"""
    # 获取工具定义（只有数学工具）
    tools = GeminiClient.build_tool_schema(ToolManager.default_tools.values())
    
    messages = [
        {"role": "system", "content": "你是一个助手。如果用户的问题可以用工具解决就调用工具，否则直接回答。"},
        {"role": "user", "content": "今天天气怎么样？"}
    ]
    
    response = await gemini_client.chat(messages, tools=tools)
    
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


@pytest.mark.asyncio
async def test_chat_empty_messages(gemini_client):
    """测试空消息列表"""
    with pytest.raises(ValueError, match="messages is required"):
        await gemini_client.chat([])


# ========== 测试用例 4: Token Usage 解析测试 ==========

@pytest.mark.asyncio
async def test_token_usage_parsing(gemini_client: GeminiClient):
    """测试 token usage 解析功能
    
    验证响应中的 token_usage 字段是否正确解析了：
    - input: 输入token数
    - output: 输出token数
    - total: 总token数
    - reasoning: 推理token数（如果存在）
    - cached: 缓存的token数（如果存在）
    """
    messages = [
        {"role": "user", "content": "请用一句话介绍人工智能。"}
    ]
    
    response = await gemini_client.chat(messages)
    
    # 验证响应
    assert response is not None
    assert response.token_usage is not None, "token_usage 应该不为 None"
    
    # 验证基本字段
    token_usage = response.token_usage
    assert "input" in token_usage, "token_usage 应包含 input 字段"
    assert "output" in token_usage, "token_usage 应包含 output 字段"
    assert "total" in token_usage, "token_usage 应包含 total 字段"
    
    # 验证字段类型
    assert isinstance(token_usage["input"], int), "input 应为整数"
    assert isinstance(token_usage["output"], int), "output 应为整数"
    assert isinstance(token_usage["total"], int), "total 应为整数"
    
    # 验证字段值合理性
    assert token_usage["input"] >= 0, "input token 数应 >= 0"
    assert token_usage["output"] >= 0, "output token 数应 >= 0"
    assert token_usage["total"] >= 0, "total token 数应 >= 0"
    
    # 验证 total 应该 >= input + output（可能包含其他token）
    assert token_usage["total"] >= token_usage["input"] + token_usage["output"], \
        f"total ({token_usage['total']}) 应 >= input ({token_usage['input']}) + output ({token_usage['output']})"
    
    # 验证可选字段（如果存在）
    if "reasoning" in token_usage:
        assert isinstance(token_usage["reasoning"], int), "reasoning 应为整数"
        assert token_usage["reasoning"] >= 0, "reasoning token 数应 >= 0"
    
    if "cached" in token_usage:
        assert isinstance(token_usage["cached"], int), "cached 应为整数"
        assert token_usage["cached"] >= 0, "cached token 数应 >= 0"
    
    print("✅ Token Usage 解析测试成功")
    print(f"   输入token数: {token_usage['input']}")
    print(f"   输出token数: {token_usage['output']}")
    print(f"   总token数: {token_usage['total']}")
    if "reasoning" in token_usage:
        print(f"   推理token数: {token_usage['reasoning']}")
    if "cached" in token_usage:
        print(f"   缓存token数: {token_usage['cached']}")
    
    # 打印完整 token_usage
    print("\n📊 完整 token_usage:")
    print(json.dumps(token_usage, ensure_ascii=False, indent=2))

