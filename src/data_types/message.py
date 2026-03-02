from dataclasses import dataclass
from enum import Enum
from typing import Any


class RoleType(Enum):
    """消息角色类型"""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

@dataclass
class Message:
    """消息类"""
    role: RoleType
    content: str
    base64_image: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[Any] | None = None  # 工具调用信息

    def to_dict(self) -> dict:
        """转换为字典格式（用于 LLM 调用）"""
        result = {"role": self.role.value, "content": self.content}
        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id
        if self.tool_calls:
            result["tool_calls"] = self.tool_calls
        return result

    @classmethod
    def user_message(cls, content: str, base64_image: str | None = None) -> "Message":
        """创建用户消息"""
        return cls(role=RoleType.USER, content=content, base64_image=base64_image)

    @classmethod
    def system_message(cls, content: str, base64_image: str | None = None) -> "Message":
        """创建系统消息"""
        return cls(role=RoleType.SYSTEM, content=content, base64_image=base64_image)

    @classmethod
    def assistant_message(
        cls,
        content: str,
        tool_calls: list[Any] | None = None,
        base64_image: str | None = None
    ) -> "Message":
        """创建助手消息"""
        return cls(role=RoleType.ASSISTANT, content=content, base64_image=base64_image, tool_calls=tool_calls)

    @classmethod
    def tool_message(cls, content: str, tool_call_id: str, base64_image: str | None = None) -> "Message":
        """创建工具消息"""
        return cls(role=RoleType.TOOL, content=content, base64_image=base64_image, tool_call_id=tool_call_id)
