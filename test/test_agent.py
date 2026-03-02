"""
AgentScope ReAct Agent 测试

测试基于 AgentScope 框架的通用 ReAct Agent 功能：
1. Agent 初始化
2. 基本对话功能
3. 工具调用功能
4. 同步和异步接口
"""

import os

import pytest

from agent.agent.agent import ReactAgentWrapper
from agentscope.tool import Toolkit


# ========== 测试用工具定义 ==========

def add(a: int, b: int) -> str:
    """计算两个整数的和"""
    return str(a + b)


def multiply(a: int, b: int) -> str:
    """计算两个整数的乘积"""
    return str(a * b)


# ========== 测试用例 ==========

def test_agent_initialization():
    """测试 Agent 初始化功能"""
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 验证环境变量已设置
    assert api_key is not None, "OPENAI_API_KEY 环境变量未设置"
    assert base_url is not None, "OPENAI_BASE_URL 环境变量未设置"
    
    # 创建 Agent
    agent = ReactAgentWrapper(
        name="TestAgent",
        model_name=model,
        api_key=api_key,
        base_url=base_url,
    )
    
    # 验证 Agent 已创建
    assert agent is not None
    assert agent.agent is not None
    assert agent.agent.name == "TestAgent"
    
    print("✅ Agent 初始化成功")
    print(f"   Agent 名称: {agent.agent.name}")
    print(f"   模型名称: {model}")


def test_agent_basic_chat():
    """测试 Agent 基本对话功能"""
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 创建 Agent
    agent = ReactAgentWrapper(
        name="ChatAgent",
        sys_prompt="你是一个友好的助手。",
        model_name=model,
        api_key=api_key,
        base_url=base_url,
    )
    
    # 测试基本对话
    response = agent.chat("你好，请简单介绍一下你自己。")
    
    # 验证响应
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    print("✅ 基本对话测试成功")
    print(f"   用户输入: 你好，请简单介绍一下你自己。")
    print(f"   Agent 回复: {response[:100]}...")


def test_agent_with_tools():
    """测试 Agent 工具调用功能"""
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 创建工具包并注册工具
    toolkit = Toolkit()
    toolkit.register_tool_function(add, name="add", description="计算两个整数的和")
    toolkit.register_tool_function(multiply, name="multiply", description="计算两个整数的乘积")
    
    # 创建带工具的 Agent
    agent = ReactAgentWrapper(
        name="ToolAgent",
        sys_prompt="你是一个数学助手。使用提供的工具来计算用户的数学问题。",
        model_name=model,
        api_key=api_key,
        base_url=base_url,
        toolkit=toolkit,
    )
    
    # 测试工具调用
    response = agent.chat("请帮我计算 15 加 27 等于多少？")
    
    # 验证响应
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    # 验证响应中包含计算结果（可能是 "42" 或包含 42 的文本）
    assert "42" in response or "42" in response.replace(" ", "")
    
    print("✅ 工具调用测试成功")
    print(f"   用户输入: 请帮我计算 15 加 27 等于多少？")
    print(f"   Agent 回复: {response}")


def test_agent_add_tool_dynamically():
    """测试动态添加工具功能"""
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 创建 Agent（初始没有工具）
    agent = ReactAgentWrapper(
        name="DynamicToolAgent",
        sys_prompt="你是一个数学助手。使用提供的工具来计算用户的数学问题。",
        model_name=model,
        api_key=api_key,
        base_url=base_url,
    )
    
    # 动态添加工具
    agent.add_tool(add, name="add", description="计算两个整数的和")
    agent.add_tool(multiply, name="multiply", description="计算两个整数的乘积")
    
    # 测试工具调用
    response = agent.chat("请帮我计算 8 乘以 7 等于多少？")
    
    # 验证响应
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    # 验证响应中包含计算结果
    assert "56" in response or "56" in response.replace(" ", "")
    
    print("✅ 动态添加工具测试成功")
    print(f"   用户输入: 请帮我计算 8 乘以 7 等于多少？")
    print(f"   Agent 回复: {response}")


def test_agent_async_chat():
    """测试 Agent 异步对话功能"""
    import asyncio
    
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 创建 Agent
    agent = ReactAgentWrapper(
        name="AsyncAgent",
        model_name=model,
        api_key=api_key,
        base_url=base_url,
    )
    
    # 定义异步测试函数
    async def run_async_test():
        # 测试异步对话
        response = await agent.chat_async("请用一句话介绍 Python 编程语言。")
        
        # 验证响应
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        
        print("✅ 异步对话测试成功")
        print(f"   用户输入: 请用一句话介绍 Python 编程语言。")
        print(f"   Agent 回复: {response[:100]}...")
        
        return response
    
    # 运行异步测试
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    response = loop.run_until_complete(run_async_test())
    
    # 再次验证响应
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


def test_agent_custom_sys_prompt():
    """测试自定义系统提示词功能"""
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 创建带自定义提示词的 Agent
    custom_prompt = "你是一个专业的代码审查助手。你的任务是帮助开发者审查代码并提供改进建议。"
    
    agent = ReactAgentWrapper(
        name="CodeReviewAgent",
        sys_prompt=custom_prompt,
        model_name=model,
        api_key=api_key,
        base_url=base_url,
    )
    
    # 验证系统提示词已设置
    assert agent.agent.sys_prompt == custom_prompt
    
    # 测试对话
    response = agent.chat("请审查这段代码：def add(a, b): return a + b")
    
    # 验证响应
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    print("✅ 自定义系统提示词测试成功")
    print(f"   系统提示词: {custom_prompt}")
    print(f"   Agent 回复: {response[:100]}...")


def test_agent_parallel_tool_calls():
    """测试并行工具调用功能"""
    # 从环境变量读取配置
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    model = os.getenv("MODEL", "gpt-4")
    
    # 创建工具包
    toolkit = Toolkit()
    toolkit.register_tool_function(add, name="add", description="计算两个整数的和")
    toolkit.register_tool_function(multiply, name="multiply", description="计算两个整数的乘积")
    
    # 创建支持并行工具调用的 Agent
    agent = ReactAgentWrapper(
        name="ParallelToolAgent",
        sys_prompt="你是一个数学助手。可以同时执行多个计算任务。",
        model_name=model,
        api_key=api_key,
        base_url=base_url,
        toolkit=toolkit,
        parallel_tool_calls=True,
    )
    
    # 测试可能需要多个工具调用的复杂问题
    response = agent.chat("请计算 10 + 20 和 5 * 6 的结果")
    
    # 验证响应
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0
    
    print("✅ 并行工具调用测试成功")
    print(f"   用户输入: 请计算 10 + 20 和 5 * 6 的结果")
    print(f"   Agent 回复: {response}")

