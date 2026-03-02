"""
LLM 调用模块

提供统一的 LLM 调用接口，基于 OpenAI SDK 实现。
支持自定义 API 地址、模型参数等配置。
"""

import asyncio
import json
import logging
import random
from typing import Any, cast, override

from json_repair import repair_json
from langsmith.wrappers import wrap_openai
from openai import AsyncOpenAI

from config import DATAHUNT_CONFIG, PROJECT_LOGGER_NAME
from llm.extra_body import ExtraBodyBuilder
from llm.llm_base import LLMClientBase, LLMConfig, LLMResponse, LLMToolCall, T

logger = logging.getLogger(f"{PROJECT_LOGGER_NAME}.{__name__}")


def _format_message(msg: dict) -> str:
    """格式化单条消息日志"""
    role = msg.get("role", "unknown")
    content = msg.get("content", "")
    tool_calls = msg.get("tool_calls")
    if tool_calls:
        return f"role={role}, content={content}, tool_calls={tool_calls}"
    elif content:
        display = content
        return f"role={role}, content={display}"
    return f"role={role}"


def _log_request(stage: str, args: dict[str, Any]) -> None:
    """记录LLM API请求日志（线程安全）"""
    lines = [
        f"📤 LLM API请求 ({stage}):",
        f"  🤖 模型: {args.get('model', 'N/A')}",
    ]
    if "temperature" in args:
        lines.append(f"  🌡️  温度: {args['temperature']}")
    if "max_tokens" in args:
        lines.append(f"  📏 最大Token: {args['max_tokens']}")
    lines.append(f"  💬 消息数量: {len(args.get('messages', []))}")
    for i, msg in enumerate(args.get("messages", [])):
        lines.append(f"    消息 {i+1}: {_format_message(msg)}")
    if args.get("tools"):
        lines.append(f"  🔧 工具数量: {len(args['tools'])}")
        for i, tool in enumerate(args["tools"]):
            tool_name = tool.get("function", {}).get("name", f"tool_{i}")
            lines.append(f"    工具 {i+1}: {tool_name}")
    logger.debug("\n".join(lines))


def _log_response(stage: str, model: str | None, parsed_response) -> None:
    """记录LLM API响应日志（线程安全）"""
    lines = [
        f"📡 LLM API响应 ({stage}):",
        f"  🤖 模型: {model}",
        f"  💬 内容: {parsed_response.content if parsed_response.content else 'None'}",
    ]
    if parsed_response.reasoning:
        reasoning = parsed_response.reasoning
        lines.append(f"  🧠 推理细节: {reasoning}")
    if parsed_response.tool_calls:
        lines.append(f"  🔧 工具调用数量: {len(parsed_response.tool_calls)}")
        for i, tc in enumerate(parsed_response.tool_calls):
            lines.append(f"    🔧 工具调用 {i+1}: {tc.name}({tc.arguments})")
    lines.append(f"  ✅ 完成原因: {parsed_response.finish_reason}")
    if parsed_response.token_usage:
        lines.append(f"  📊 Token使用: {parsed_response.token_usage}")
    if parsed_response.refused_reason:
        lines.append(f"  ⚠️  拒绝原因: {parsed_response.refused_reason}")
    logger.debug("\n".join(lines))


class OpenAIClient(LLMClientBase):
    """
    LLM 客户端

    基于 OpenAI SDK 的统一 LLM 调用接口，支持 OpenAI 及兼容 API。

    使用示例:
    ```python
    from llm.llm_base import LLMConfig
    from llm.openai import OpenAIClient

    config = LLMConfig(
        api_key="your-api-key",
        base_url="https://api.openai.com/v1",
        model="gpt-4"
    )
    llm = OpenAIClient(config)

    # 异步对话
    response = await llm.chat(messages)

    # 工具调用
    response = await llm.chat(messages, tools=tools)

    # 结构化输出
    result = await llm.chat_structured_output(messages, response_format=MyModel)
    ```
    """

    def initialize_client(self):
        """
        初始化 OpenAI SDK 异步客户端，使用官方 SDK 内置的重试机制
        """
        if not self._config.api_key:
            raise ValueError("API Key 未配置")

        self._client = wrap_openai(AsyncOpenAI(
            api_key=self._config.api_key,
            base_url=self._config.base_url,
            max_retries=self._config.max_retries,  # 使用官方 SDK 内置重试机制
            timeout=self._config.timeout  # 设置超时时间
        ))

    @override
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
        if not messages:
            raise ValueError("messages is required")

        args: dict[str, Any] = {
            "messages": messages,
            "model": model or self._config.model,
        }

        if temperature is not None:
            args["temperature"] = temperature
        elif self._config.temperature is not None:
            args["temperature"] = self._config.temperature

        if max_tokens is not None:
            args["max_tokens"] = max_tokens
        elif self._config.max_tokens is not None:
            args["max_tokens"] = self._config.max_tokens

        if tools:
            args["tools"] = tools

        # 构建 extra_body
        if self._config.extra_body or "extra_body" in kwargs:
            builder = ExtraBodyBuilder()

            # 合并配置中的 extra_body
            if self._config.extra_body:
                builder.merge(self._config.extra_body)

            # 如果 kwargs 中已有 extra_body，需要合并
            if "extra_body" in kwargs:
                existing_extra_body = kwargs.pop("extra_body")
                if isinstance(existing_extra_body, dict):
                    builder.merge(existing_extra_body)

            args["extra_body"] = builder.build()

        args.update(kwargs)

        _log_request("chat", args)

        # 使用原生异步 API
        response = await self._client.chat.completions.create(**args)

        # 解析响应
        parsed_response = self._parse_response(response)

        _log_response("chat", args.get("model"), parsed_response)

        return parsed_response

    @override
    async def chat_structured_output(
        self,
        messages: list[dict],
        *,
        response_format: type[T],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        parse_api: bool = False,
        **kwargs
    ) -> T:
        """
        异步结构化输出方法

        根据 parse_api 参数路由到不同的实现：
        - parse_api=True: 使用 chat.completions.parse API（推荐，更高效）
        - parse_api=False: 使用 chat.completions.create API + extra_body + 手动解析

        Args:
            messages: 消息列表
            response_format: Pydantic BaseModel 子类，定义输出结构
            model: 模型名称
            temperature: 温度参数
            max_tokens: 最大返回 token 数
            parse_api: 是否使用 parse API，True 使用 parse API，False 使用 create API + extra_body
            **kwargs: 其他参数

        Returns:
            T: 解析后的结构化对象，类型由 response_format 决定
        """
        if parse_api:
            return await self._parse_structured_output(
                messages=messages,
                response_format=response_format,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        else:
            return await self._chat_structured_output(
                messages=messages,
                response_format=response_format,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

    async def _parse_structured_output(
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
        私有方法：使用 chat.completions.parse API 的结构化输出

        将 LLM 响应解析为指定的 Pydantic 模型，解析失败时自动重试。

        Args:
            参数说明同 chat_structured_output

        Returns:
            T: 解析后的结构化对象，类型由 response_format 决定
        """
        if not messages:
            raise ValueError("messages is required")
        if not response_format:
            raise ValueError("response_format is required")

        max_retries = self._config.max_retries
        last_error = None
        response: Any = None  # 预先初始化，用于错误日志
        # 指数退避初始延迟（秒）
        base_delay = 2.0

        for attempt in range(max_retries + 1):
            try:
                args = {
                    "messages": messages,
                    "model": model or self._config.model,
                    "response_format": response_format,
                }

                if temperature is not None:
                    args["temperature"] = temperature
                elif self._config.temperature is not None:
                    args["temperature"] = self._config.temperature

                if max_tokens is not None:
                    args["max_tokens"] = max_tokens
                elif self._config.max_tokens is not None:
                    args["max_tokens"] = self._config.max_tokens

                # 构建 extra_body
                if self._config.extra_body or "extra_body" in kwargs:
                    builder = ExtraBodyBuilder()

                    # 合并配置中的 extra_body
                    if self._config.extra_body:
                        builder.merge(self._config.extra_body)

                    # 如果 kwargs 中已有 extra_body，需要合并
                    if "extra_body" in kwargs:
                        existing_extra_body = kwargs.pop("extra_body")
                        if isinstance(existing_extra_body, dict):
                            builder.merge(existing_extra_body)

                    args["extra_body"] = builder.build()

                args.update(kwargs)

                _log_request("parse_structured", args)

                # 使用原生异步 API
                response = await self._client.chat.completions.parse(**args)

                parsed_response = self._parse_response(response)

                _log_response("parse_structured", args.get("model"), parsed_response)

                if parsed_response.parsed is None:
                    raise ValueError("未能解析结构化输出")

                if parsed_response.parsed:
                    parsed_json = parsed_response.parsed.model_dump_json(ensure_ascii=False, indent=2)
                    logger.debug(f"  📋 解析结果: {parsed_json}")

                return cast(T, parsed_response.parsed)

            except Exception as e:
                last_error = e
                # 打印原始响应以便调试
                try:
                    logger.error(f"结构化输出解析失败，原始响应: {response}")
                except NameError:
                    logger.error("结构化输出解析失败，API 调用未返回响应")
                if attempt < max_retries:
                    # 指数退避：delay = base_delay * 2^attempt，添加随机抖动
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    logger.warning(f"结构化输出解析失败，{delay:.2f}s 后尝试第 {attempt + 2}/{max_retries + 1} 次重试: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"结构化输出解析失败，已达到最大重试次数 {max_retries}: {e}")

        raise ValueError(f"结构化输出解析失败，已达到最大重试次数 {max_retries}: {last_error}")

    async def _chat_structured_output(
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
        私有方法：使用 chat.completions.create API + extra_body 的结构化输出

        使用 chat.completions.create API 配合 extra_body 传递 json_schema，
        并在函数内解析 JSON 响应为指定的 Pydantic 模型，解析失败时自动重试。

        Args:
            参数说明同 chat_structured_output

        Returns:
            T: 解析后的结构化对象，类型由 response_format 决定
        """
        if not messages:
            raise ValueError("messages is required")
        if not response_format:
            raise ValueError("response_format is required")

        max_retries = self._config.max_retries
        last_error = None
        response: Any = None  # 预先初始化，用于错误日志
        # 指数退避初始延迟（秒）
        base_delay = 2.0

        for attempt in range(max_retries + 1):
            try:
                args = {
                    "messages": messages,
                    "model": model or self._config.model,
                }

                if temperature is not None:
                    args["temperature"] = temperature
                elif self._config.temperature is not None:
                    args["temperature"] = self._config.temperature

                if max_tokens is not None:
                    args["max_tokens"] = max_tokens
                elif self._config.max_tokens is not None:
                    args["max_tokens"] = self._config.max_tokens

                # 构建 extra_body，包含 json_schema
                builder = ExtraBodyBuilder()

                # 添加 json_schema 到 extra_body
                builder.with_json_schema(model=response_format)

                # 合并配置中的 extra_body
                if self._config.extra_body:
                    builder.merge(self._config.extra_body)

                # 如果 kwargs 中已有 extra_body，需要合并
                if "extra_body" in kwargs:
                    existing_extra_body = kwargs.pop("extra_body")
                    if isinstance(existing_extra_body, dict):
                        builder.merge(existing_extra_body)

                args["extra_body"] = builder.build()

                args.update(kwargs)

                _log_request("create_structured", args)

                # 使用 chat.completions.create API
                response = await self._client.chat.completions.create(**args)

                parsed_response = self._parse_response(response)

                _log_response("create_structured", args.get("model"), parsed_response)

                # 手动解析 JSON 并转换为 Pydantic 模型
                if not parsed_response.content:
                    logger.error(f"响应内容为空，无法解析结构化输出: {parsed_response}")
                    raise ValueError("响应内容为空，无法解析结构化输出")

                # 使用 json-repair 解析 JSON 字符串
                json_data = repair_json(parsed_response.content, return_objects=True)
                # 转换为 Pydantic 模型
                parsed_model = response_format.model_validate(json_data)
                parsed_json = parsed_model.model_dump_json(ensure_ascii=False, indent=2)
                logger.debug(f"  📋 解析结果: {parsed_json}")
                return parsed_model

            except Exception as e:
                last_error = e
                # 打印原始响应以便调试
                try:
                    logger.error(f"结构化输出解析失败，原始响应: {response}")
                except NameError:
                    logger.error("结构化输出解析失败，API 调用未返回响应")
                if attempt < max_retries:
                    # 指数退避：delay = base_delay * 2^attempt，添加随机抖动
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
                    logger.warning(f"结构化输出解析失败，{delay:.2f}s 后尝试第 {attempt + 2}/{max_retries + 1} 次重试: {e}")
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"结构化输出解析失败，已达到最大重试次数 {max_retries}: {e}")

        raise ValueError(f"结构化输出解析失败，已达到最大重试次数 {max_retries}: {last_error}")

    def _parse_response(self, response) -> LLMResponse:
        """
        解析 OpenAI API 响应为 LLMResponse

        Args:
            response: OpenAI API 响应对象

        Returns:
            LLMResponse 对象
        """
        choice = response.choices[0]
        message = choice.message
        parsed = getattr(message, "parsed", None)
        tool_calls = []

        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(LLMToolCall(
                    id=tc.id,
                    name=tc.function.name,
                    arguments=json.loads(tc.function.arguments)
                ))

        # 确定 finish_reason
        finish_reason = choice.finish_reason
        if tool_calls and finish_reason != "tool_calls":
            finish_reason = "tool_calls"

        # 解析推理细节
        reasoning = None
        if hasattr(message, "reasoning") and message.reasoning:
            # reasoning 可能是字符串或对象，需要根据实际结构提取
            if isinstance(message.reasoning, str):
                reasoning = message.reasoning
            elif hasattr(message.reasoning, "content"):
                reasoning = message.reasoning.content
            elif isinstance(message.reasoning, dict):
                reasoning = message.reasoning.get("content") or str(message.reasoning)

        # 解析 token usage
        # 根据 llm_base.py 注释：记录输入token数、输出token数、推理token数、总花费token数、cached token数
        token_usage = None
        if response.usage:
            token_usage = {
                "input": getattr(response.usage, "prompt_tokens", 0),
                "output": getattr(response.usage, "completion_tokens", 0),
                "total": getattr(response.usage, "total_tokens", 0),
            }
            # 某些 API 可能支持推理 token（位于 completion_tokens_details 中）
            if hasattr(response.usage, "completion_tokens_details"):
                details = response.usage.completion_tokens_details
                if hasattr(details, "reasoning_tokens"):
                    token_usage["reasoning"] = details.reasoning_tokens
            # 某些 API 可能支持缓存 token（位于 prompt_tokens_details 中）
            if hasattr(response.usage, "prompt_tokens_details"):
                details = response.usage.prompt_tokens_details
                if hasattr(details, "cached_tokens"):
                    token_usage["cached"] = details.cached_tokens

        return LLMResponse(
            content=message.content or "",
            raw_response=response,
            tool_calls=tool_calls if tool_calls else None,
            parsed=parsed,
            finish_reason=finish_reason or "",
            refused_reason=message.refusal,
            token_usage=token_usage,
            reasoning=reasoning
        )

    @staticmethod
    def parse_tool_calls(response) -> list[LLMToolCall]:
        """
        解析 LLM 响应中的工具调用

        Args:
            response: OpenAI API 响应对象

        Returns:
            list[LLMToolCall]: 工具调用列表
        """
        tool_calls: list[LLMToolCall] = []

        if not hasattr(response, 'choices') or not response.choices:
            return tool_calls

        message = response.choices[0].message

        if not hasattr(message, 'tool_calls') or not message.tool_calls:
            return tool_calls

        for tc in message.tool_calls:
            try:
                tool_calls.append(LLMToolCall(
                    id=tc.id,
                    name=tc.function.name,
                arguments=json.loads(tc.function.arguments)
                ))
            except Exception as e:
                logger.warning(f"解析工具调用失败: {e}")

        return tool_calls


openai_client = OpenAIClient(LLMConfig(
    api_key=DATAHUNT_CONFIG.OPENAI_API_KEY,
    base_url=DATAHUNT_CONFIG.OPENAI_BASE_URL,
    model=DATAHUNT_CONFIG.OPENAI_MODEL,
    temperature=0.0,
    max_tokens=2048,
    max_retries=DATAHUNT_CONFIG.LLM_MAX_RETRIES,
    extra_body=ExtraBodyBuilder().with_seed(42).with_reasoning(False).build()
))

skeleton_extractor_client = OpenAIClient(LLMConfig(
    api_key=DATAHUNT_CONFIG.SKELETON_EXTRACTOR_API_KEY,
    base_url=DATAHUNT_CONFIG.SKELETON_EXTRACTOR_BASE_URL,
    model=DATAHUNT_CONFIG.SKELETON_EXTRACTOR_MODEL,
    temperature=0.0,
    max_tokens=2048,
    max_retries=DATAHUNT_CONFIG.LLM_MAX_RETRIES,
    extra_body=ExtraBodyBuilder().with_seed(42).with_reasoning(False).build()
))

sql_generator_client = OpenAIClient(LLMConfig(
    api_key=DATAHUNT_CONFIG.SQL_API_KEY,
    base_url=DATAHUNT_CONFIG.SQL_BASE_URL,
    model=DATAHUNT_CONFIG.SQL_MODEL,
    temperature=0.0,
    max_tokens=4096,
    max_retries=DATAHUNT_CONFIG.LLM_MAX_RETRIES,
    extra_body=ExtraBodyBuilder().with_seed(42).with_reasoning(False).build()
))

sql_fix_client = OpenAIClient(LLMConfig(
    api_key=DATAHUNT_CONFIG.SQL_API_KEY,
    base_url=DATAHUNT_CONFIG.SQL_BASE_URL,
    model=DATAHUNT_CONFIG.SQL_MODEL,
    temperature=0.0,
    max_tokens=4096,
    max_retries=DATAHUNT_CONFIG.LLM_MAX_RETRIES,
    extra_body=ExtraBodyBuilder().with_seed(42).with_reasoning(False).build()
))

sql_fix_final_client = OpenAIClient(LLMConfig(
    api_key=DATAHUNT_CONFIG.SQL_API_KEY,
    base_url=DATAHUNT_CONFIG.SQL_BASE_URL,
    model=DATAHUNT_CONFIG.SQL_MODEL,
    temperature=0.0,
    max_tokens=10000,
    max_retries=DATAHUNT_CONFIG.LLM_MAX_RETRIES,
    extra_body=ExtraBodyBuilder().with_seed(42).with_reasoning().build()
))

query_rewrite_client = OpenAIClient(LLMConfig(
    api_key=DATAHUNT_CONFIG.REWRITE_API_KEY,
    base_url=DATAHUNT_CONFIG.REWRITE_BASE_URL,
    model=DATAHUNT_CONFIG.REWRITE_MODEL,
    temperature=0.0,
    max_tokens=2048,
    max_retries=DATAHUNT_CONFIG.LLM_MAX_RETRIES,
    extra_body=ExtraBodyBuilder().with_seed(42).with_reasoning(False).build()
))
