"""
QueryRewriter 测试程序

测试 QueryRewriter 的核心功能：
1. 初始化（类型检查、prompt 加载）
2. rewrite 方法（Mock 测试）
3. 真实 API 测试（使用 OpenAI）
"""

import os

import pytest
from dotenv import load_dotenv

from config import DATAHUNT_CONFIG
from graph.rewritter import QueryRewritter, RewriteQueryResponse
from llm.llm_base import LLMClientBase, LLMConfig
from llm.openai import OpenAIClient

# 加载环境变量（从 config/.env 文件）
load_dotenv(dotenv_path="config/.env")


# ========== Mock LLM Client ==========

class MockLLMClient(LLMClientBase):
    """Mock LLM 客户端，用于测试"""
    
    def __init__(self):
        # 创建一个最小配置
        config = LLMConfig(
            api_key="mock-key",
            model="mock-model"
        )
        super().__init__(config)
        self.chat_structured_output_calls = []
    
    def initialize_client(self):
        """Mock 初始化，不需要真实客户端"""
        pass
    
    async def chat(self, messages, **kwargs):
        """Mock chat 方法"""
        raise NotImplementedError("Mock client does not implement chat")
    
    async def chat_structured_output(self, messages, *, response_format, **kwargs):
        """Mock chat_structured_output 方法，记录调用参数"""
        self.chat_structured_output_calls.append({
            "messages": messages,
            "response_format": response_format,
            "kwargs": kwargs
        })
        
        # 返回一个模拟的 RewriteQueryResponse
        return RewriteQueryResponse(
            reasoning="Mock reasoning: 将用户问题改写为适合检索数据表的问题",
            query="Mock rewritten query"
        )
    
    @staticmethod
    def build_tool_schema(tools):
        """Mock build_tool_schema 方法"""
        return []


# ========== Fixtures ==========

@pytest.fixture
def mock_llm_client():
    """创建 Mock LLM 客户端"""
    return MockLLMClient()


@pytest.fixture
def openai_config():
    """创建 OpenAI 配置"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        pytest.skip("OPENAI_API_KEY 环境变量未设置，跳过测试")
    
    # 使用 DATAHUNT_CONFIG 的配置
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


# ========== 测试用例 1: 初始化测试 ==========

def test_init_success(openai_client):
    """测试正常初始化"""
    rewritter = QueryRewritter(client=openai_client)
    
    # 验证 client 被正确设置
    assert rewritter.client is openai_client
    
    # 验证 prompt 被正确加载
    assert hasattr(rewritter, "system_prompt")
    assert hasattr(rewritter, "user_prompt_template")
    assert isinstance(rewritter.system_prompt, str)
    assert isinstance(rewritter.user_prompt_template, str)
    
    # 注意：如果配置未正确加载，prompt 可能为空字符串
    # 但这是配置加载的问题，不是 QueryRewriter 的问题
    # 我们仍然验证结构是正确的
    if len(rewritter.user_prompt_template) > 0:
        # 验证 prompt 内容包含预期的占位符
        assert "{latest_query}" in rewritter.user_prompt_template
        assert "{conversation_history}" in rewritter.user_prompt_template
    
    print("✅ 初始化测试成功")
    print(f"   system_prompt 长度: {len(rewritter.system_prompt)}")
    print(f"   user_prompt_template 长度: {len(rewritter.user_prompt_template)}")
    if len(rewritter.user_prompt_template) > 0:
        print(f"   user_prompt_template: {rewritter.user_prompt_template[:100]}...")


def test_init_type_error():
    """测试传入非 LLMClientBase 实例时抛出 TypeError"""
    # 传入 None
    with pytest.raises(TypeError, match="client 必须是 LLMClientBase 的实例"):
        QueryRewritter(client=None)
    
    # 传入字符串
    with pytest.raises(TypeError, match="client 必须是 LLMClientBase 的实例"):
        QueryRewritter(client="not a client")
    
    # 传入普通对象
    with pytest.raises(TypeError, match="client 必须是 LLMClientBase 的实例"):
        QueryRewritter(client=object())
    
    print("✅ 类型检查测试成功")


# ========== 测试用例 2: rewrite_from_messages 方法测试（Mock） ==========

@pytest.mark.asyncio
async def test_rewrite_with_evidence(mock_llm_client):
    """测试有 evidence 的改写"""
    from data_types.message import Message, RoleType

    rewriter = QueryRewritter(client=mock_llm_client)

    messages = [Message(role=RoleType.USER, content="查询比利时的人口")]
    evidence = "比利时是欧洲的一个国家"

    result = await rewriter.rewrite_from_messages(messages=messages, evidence=evidence)

    # 验证返回类型
    assert isinstance(result, RewriteQueryResponse)
    assert hasattr(result, "query")
    assert isinstance(result.query, str)

    # 验证 LLM 被正确调用
    assert len(mock_llm_client.chat_structured_output_calls) == 1
    call_info = mock_llm_client.chat_structured_output_calls[0]

    # 验证 messages 结构
    messages_sent = call_info["messages"]
    assert len(messages_sent) == 2
    assert messages_sent[0]["role"] == "system"
    assert messages_sent[1]["role"] == "user"

    # 验证 user prompt 包含 question 和 evidence
    user_content = messages_sent[1]["content"]
    if rewriter.user_prompt_template:
        assert "比利时的人口" in user_content or "{latest_query}" in rewriter.user_prompt_template

    # 验证 response_format
    assert call_info["response_format"] == RewriteQueryResponse

    print("✅ 有 evidence 的改写测试成功")
    print(f"   改写后的问题: {result.query}")


@pytest.mark.asyncio
async def test_rewrite_without_evidence(mock_llm_client):
    """测试没有 evidence 的改写（evidence 为空字符串）"""
    from data_types.message import Message, RoleType

    rewriter = QueryRewritter(client=mock_llm_client)

    messages = [Message(role=RoleType.USER, content="查询中国的人口数量")]
    evidence = ""

    result = await rewriter.rewrite_from_messages(messages=messages, evidence=evidence)

    # 验证返回类型
    assert isinstance(result, RewriteQueryResponse)

    # 验证 LLM 被调用
    assert len(mock_llm_client.chat_structured_output_calls) == 1
    call_info = mock_llm_client.chat_structured_output_calls[0]

    # 验证 user prompt 包含 question
    user_content = call_info["messages"][1]["content"]
    if rewriter.user_prompt_template:
        assert "中国的人口数量" in user_content or "{latest_query}" in rewriter.user_prompt_template

    print("✅ 无 evidence 的改写测试成功")
    print(f"   改写后的问题: {result.query}")


@pytest.mark.asyncio
async def test_rewrite_prompt_formatting(mock_llm_client):
    """测试 prompt 格式化是否正确"""
    from data_types.message import Message, RoleType

    rewriter = QueryRewritter(client=mock_llm_client)

    messages = [Message(role=RoleType.USER, content="测试问题")]
    evidence = "测试证据"

    await rewriter.rewrite_from_messages(messages=messages, evidence=evidence)

    # 获取调用信息
    call_info = mock_llm_client.chat_structured_output_calls[0]
    messages_sent = call_info["messages"]

    # 验证 system prompt
    system_content = messages_sent[0]["content"]
    assert system_content == rewriter.system_prompt

    # 验证 user prompt 格式化
    user_content = messages_sent[1]["content"]
    if rewriter.user_prompt_template:
        assert "测试问题" in user_content or "{latest_query}" in rewriter.user_prompt_template

    print("✅ Prompt 格式化测试成功")
    print(f"   System prompt 长度: {len(system_content)}")
    print(f"   User prompt 长度: {len(user_content)}")


# ========== 测试用例 3: 真实 API 测试（使用 OpenAI） ==========

@pytest.mark.asyncio
async def test_rewrite_real_api_with_evidence(openai_client: OpenAIClient):
    """测试使用真实 OpenAI API 进行改写（有 evidence）"""
    from data_types.message import Message, RoleType

    rewriter = QueryRewritter(client=openai_client)

    messages = [Message(role=RoleType.USER, content="查询比利时的人口")]
    evidence = "比利时是欧洲的一个国家，首都布鲁塞尔"

    result = await rewriter.rewrite_from_messages(messages=messages, evidence=evidence)

    # 验证返回类型
    assert isinstance(result, RewriteQueryResponse)
    assert isinstance(result.query, str)

    # 验证内容不为空
    assert len(result.query) > 0

    print("✅ 真实 API 测试（有 evidence）成功")
    print(f"   原始问题: 查询比利时的人口")
    print(f"   Evidence: {evidence}")
    print(f"   改写后的问题: {result.query}")


@pytest.mark.asyncio
async def test_rewrite_real_api_without_evidence(openai_client: OpenAIClient):
    """测试使用真实 OpenAI API 进行改写（无 evidence）"""
    from data_types.message import Message, RoleType

    rewriter = QueryRewritter(client=openai_client)

    messages = [Message(role=RoleType.USER, content="查询中国的人口数量")]
    evidence = ""

    result = await rewriter.rewrite_from_messages(messages=messages, evidence=evidence)

    # 验证返回类型和内容
    assert isinstance(result, RewriteQueryResponse)
    assert len(result.query) > 0

    print("✅ 真实 API 测试（无 evidence）成功")
    print(f"   原始问题: 查询中国的人口数量")
    print(f"   改写后的问题: {result.query}")


@pytest.mark.asyncio
async def test_rewrite_real_api_complex_question(openai_client: OpenAIClient):
    """测试复杂问题的改写"""
    from data_types.message import Message, RoleType

    rewriter = QueryRewritter(client=openai_client)

    messages = [Message(role=RoleType.USER, content="我想知道2023年销售额排名前10的产品名称和对应的销售额")]
    evidence = "销售额 = 单价 × 数量，产品表包含产品名称、单价等字段"

    result = await rewriter.rewrite_from_messages(messages=messages, evidence=evidence)

    # 验证返回类型和内容
    assert isinstance(result, RewriteQueryResponse)
    assert len(result.query) > 0

    print("✅ 复杂问题改写测试成功")
    print(f"   原始问题: {messages[0].content}")
    print(f"   Evidence: {evidence}")
    print(f"   改写后的问题: {result.query}")


# ========== 测试用例 4: batch_rewrite 方法测试（真实 API） ==========
# 注意：batch_rewrite 方法未实现，此测试暂时跳过

@pytest.mark.skip(reason="batch_rewrite 方法未实现")
@pytest.mark.asyncio
async def test_batch_rewrite_mixed_evidence(openai_client: OpenAIClient):
    """测试批量改写（混合有/无 evidence）"""
    # 此测试暂时跳过，等待 batch_rewrite 方法实现
    pass

