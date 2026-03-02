import logging
from abc import ABC, abstractmethod
from typing import Any, TypeVar

from pydantic import BaseModel, Field

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")

class LLMConfig(BaseModel):
    """ LLMClient 配置 """
    api_key: str
    model: str
    base_url: str | None = None
    temperature: float = 0.0
    max_tokens: int | None = None
    timeout: int = 60
    extra_body: dict[str, Any] | None = None  # 额外的请求参数，支持 seed、reasoning 等
    max_retries: int = Field(default_factory=lambda: DATAHUNT_CONFIG.LLM_MAX_RETRIES)  # API 调用最大重试次数，默认使用配置值

class LLMToolCall(BaseModel):
    """ LLM API返回的工具调用 """
    id: str
    name: str
    arguments: dict

class LLMResponse(BaseModel):
    """ LLM API返回的响应 """
    content: str
    raw_response: Any # 保留原始响应以便调试
    tool_calls: list[LLMToolCall] | None
    parsed: BaseModel | None
    finish_reason: str
    refused_reason: str | None
    token_usage: dict[str, int] | None = None # 记录输入token数、输出token数、推理token数、总花费token数、cached token数
    reasoning: str | None = None # 推理细节内容


T = TypeVar("T", bound=BaseModel)


class LLMClientBase(ABC):
    """
    LLM 客户端基类

    定义统一的异步接口，包括：
    1. 异步工具调用（无工具时为正常对话）
    2. 结构化输出
    """

    def __init__(self, config: LLMConfig):
        """
        初始化配置参数，子类不需要实现该方法

        Args:
            config: LLM 配置对象
        """
        self._config = config
        self.initialize_client()

    @abstractmethod
    def initialize_client(self):
        """
        子类只需要实现这个方法来初始化具体的 SDK 客户端。
        不需要实现 __init__。
        """
        pass


    @abstractmethod
    async def chat(
        self,
        messages: list[dict],
        *,
        tools: list[dict] | None = None,
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs
    ) -> LLMResponse:
        """
        异步对话方法，支持工具调用

        当 tools 为 None 时，执行正常对话；当 tools 不为 None 时，执行工具调用。

        Args:
            messages: 消息列表
            tools: 工具定义列表（OpenAI tools 格式），None 时执行正常对话
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大返回 token 数
            **kwargs: 其他参数

        Returns:
            LLMResponse: 包含 content、tool_calls 等信息的响应对象
        """
        pass

    @abstractmethod
    async def chat_structured_output(
        self,
        messages: list[dict],
        *,
        response_format: type[T],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        **kwargs
    ) -> T:
        """
        异步结构化输出方法

        将 LLM 响应解析为指定的 Pydantic 模型。

        Args:
            messages: 消息列表
            response_format: Pydantic BaseModel 子类，定义输出结构
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大返回 token 数
            **kwargs: 其他参数

        Returns:
            T: 解析后的结构化对象，类型由 response_format 决定
        """
        pass
