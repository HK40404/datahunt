"""
Base Tool 抽象基类

所有工具的基类，包含工具的基本属性和接口。
类方法设计，无需实例化。
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """工具抽象基类（类方法设计）"""

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        """工具名称"""
        pass

    @classmethod
    @abstractmethod
    def description(cls) -> str:
        """工具描述"""
        pass

    @classmethod
    @abstractmethod
    def parameters(cls) -> dict[str, Any]:
        """工具参数 schema（OpenAI function calling 格式）"""
        pass

    @classmethod
    @abstractmethod
    def invoke(cls, **kwargs) -> str:
        """
        执行工具逻辑

        Args:
            **kwargs: 工具参数

        Returns:
            str: 执行结果
        """
        pass

    @classmethod
    def get_schema(cls) -> dict[str, Any]:
        """
        获取 OpenAI tools 格式的工具定义

        Returns:
            dict: OpenAI function calling 格式的工具定义
        """
        if cls != BaseTool:
            return {
                "type": "function",
                "function": {
                    "name": cls.name(),
                    "description": cls.description(),
                    "parameters": cls.parameters()
                }
            }

        return {
            "type": "function",
            "function": {
                "name": "unknown_tool",
                "description": "Unknown tool",
                "parameters": {}
            }
        }


class ToolSet:
    """工具集合，管理工具类的查询和 schema 生成"""

    def __init__(self, tools: list[type[BaseTool]]):
        """
        初始化工具集合

        Args:
            tools: 工具类列表
        """
        self._tools: dict[str, type[BaseTool]] = {tool.name(): tool for tool in tools}

    def get_schemas(self) -> list[dict[str, Any]]:
        """
        获取所有工具的 OpenAI 格式 schema

        Returns:
            list: 工具 schema 列表
        """
        return [tool_class.get_schema() for tool_class in self._tools.values()]

    def get_tool(self, name: str) -> type[BaseTool] | None:
        """
        根据名称获取工具类

        Args:
            name: 工具名称

        Returns:
            Tool class if found, None otherwise
        """
        return self._tools.get(name)
