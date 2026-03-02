"""
OpenAI SDK extra_body 参数构建工具

提供用于构建 OpenAI SDK extra_body 参数的类，支持结构化输出等功能。
"""

from typing import Any

from pydantic import BaseModel


class ExtraBodyBuilder:
    """
    构建 OpenAI SDK extra_body 参数的类

    支持将 Pydantic BaseModel 转换为结构化输出的 JSON schema 格式。

    使用示例:
    ```python
    from pydantic import BaseModel, Field

    class SentimentAnalysis(BaseModel):
        sentiment: str = Field(..., description="情感倾向")
        confidence: float = Field(..., description="置信度")

    builder = ExtraBodyBuilder()
    extra_body = builder.with_json_schema(
        model=SentimentAnalysis,
        name="sentiment_analysis",
        strict=True
    ).with_provider().build()

    response = client.chat.completions.create(
        model="openai/gpt-5-mini",
        messages=[{"role": "user", "content": "..."}],
        extra_body=extra_body
    )
    ```
    """

    def __init__(self):
        """初始化 ExtraBodyBuilder"""
        self._extra_body: dict[str, Any] = {}

    def with_json_schema(
        self,
        model: type[BaseModel],
        name: str | None = None,
        strict: bool = True
    ) -> "ExtraBodyBuilder":
        """
        添加结构化输出的 JSON schema 配置

        Args:
            model: Pydantic BaseModel 类
            name: schema 名称，如果为 None 则使用模型类名（转换为 snake_case）
            strict: 是否启用严格模式

        Returns:
            self，支持链式调用
        """
        if not issubclass(model, BaseModel):
            raise TypeError(f"model 必须是 BaseModel 的子类，当前类型: {type(model)}")

        # 获取 JSON schema
        json_schema = model.model_json_schema()

        # 移除所有 title 字段（OpenAI 不需要）
        self._remove_titles(json_schema)

        # 确定 schema 名称
        schema_name = name or self._get_default_schema_name(model)

        # 构建 response_format
        self._extra_body["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": strict,
                "schema": json_schema
            }
        }

        return self

    def with_reasoning(self, enabled: bool = True) -> "ExtraBodyBuilder":
        """
        添加推理功能配置

        Args:
            enabled: 是否启用推理功能

        Returns:
            self，支持链式调用
        """
        if "reasoning" not in self._extra_body:
            self._extra_body["reasoning"] = {}

        self._extra_body["reasoning"]["enabled"] = enabled
        return self

    def with_provider(self, require_parameters: bool = True) -> "ExtraBodyBuilder":
        """
        添加 provider 配置

        Args:
            require_parameters: 是否要求参数

        Returns:
            self，支持链式调用
        """
        if "provider" not in self._extra_body:
            self._extra_body["provider"] = {}

        self._extra_body["provider"]["require_parameters"] = require_parameters
        return self

    def with_seed(self, seed: int) -> "ExtraBodyBuilder":
        """
        设置 seed 参数用于确定性输出

        相同的 seed 和请求参数应该返回相同结果。注意：determinism 不保证对所有模型有效。

        Args:
            seed: 整数 seed 值

        Returns:
            self，支持链式调用
        """
        self._extra_body["seed"] = seed
        return self

    def with_custom(self, key: str, value: Any) -> "ExtraBodyBuilder":
        """
        添加自定义参数

        Args:
            key: 参数名
            value: 参数值

        Returns:
            self，支持链式调用
        """
        self._extra_body[key] = value
        return self

    def merge(self, other: dict[str, Any]) -> "ExtraBodyBuilder":
        """
        合并其他 extra_body 字典

        如果遇到配置冲突，保留主体 ExtraBodyBuilder 中已设置的值，忽略 other 中的冲突值。
        新键会被添加，已存在的键不会被覆盖。

        Args:
            other: 要合并的字典

        Returns:
            self，支持链式调用
        """
        # 深度合并字典，保留主体 ExtraBodyBuilder 的值
        self._deep_merge(self._extra_body, other)
        return self

    def build(self) -> dict[str, Any]:
        """
        构建并返回 extra_body 字典

        Returns:
            extra_body 字典
        """
        return self._extra_body.copy()

    @staticmethod
    def _get_default_schema_name(model: type[BaseModel]) -> str:
        """
        获取默认的 schema 名称（将类名转换为 snake_case）

        Args:
            model: Pydantic BaseModel 类

        Returns:
            snake_case 格式的类名
        """
        class_name = model.__name__
        # 简单的驼峰转蛇形命名
        result = []
        for i, char in enumerate(class_name):
            if char.isupper() and i > 0:
                result.append('_')
            result.append(char.lower())
        return ''.join(result)

    @staticmethod
    def _remove_titles(schema: dict[str, Any]) -> None:
        """
        递归移除 schema 中的所有 title 字段

        Args:
            schema: JSON schema 字典（会被修改）
        """
        if isinstance(schema, dict):
            schema.pop("title", None)
            for value in schema.values():
                if isinstance(value, dict):
                    ExtraBodyBuilder._remove_titles(value)
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            ExtraBodyBuilder._remove_titles(item)

    @staticmethod
    def _deep_merge(base: dict[str, Any], update: dict[str, Any]) -> None:
        """
        深度合并两个字典（保留主体 base 的值）

        如果键已存在，保留 base 中的值；如果键不存在，添加 update 中的值。
        对于嵌套字典，递归合并。

        Args:
            base: 基础字典（会被修改），主体 ExtraBodyBuilder 的值
            update: 要合并的字典
        """
        for key, value in update.items():
            if key not in base:
                # 新键直接添加
                base[key] = value
            elif isinstance(base[key], dict) and isinstance(value, dict):
                # 两个值都是字典，递归合并
                ExtraBodyBuilder._deep_merge(base[key], value)
            # 如果键已存在且不是字典，保留 base 中的原值（不覆盖）
