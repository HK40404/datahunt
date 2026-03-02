"""
Message 数据类型测试

测试消息类型定义和操作
"""

import pytest

from data_types.message import Message, RoleType


class TestMessage:
    """Message 测试类"""

    def test_message_creation(self):
        """测试消息创建"""
        msg = Message(role=RoleType.USER, content="Hello")
        assert msg.role == RoleType.USER
        assert msg.content == "Hello"

    def test_message_role_types(self):
        """测试角色类型"""
        assert RoleType.USER.value == "user"
        assert RoleType.ASSISTANT.value == "assistant"
        assert RoleType.SYSTEM.value == "system"

    def test_message_to_dict(self):
        """测试消息转换为字典"""
        msg = Message(role=RoleType.USER, content="Test")
        msg_dict = msg.to_dict()
        assert isinstance(msg_dict, dict)
        assert msg_dict["role"] == "user"
        assert msg_dict["content"] == "Test"

    def test_message_with_tool_calls(self):
        """测试带工具调用的消息"""
        tool_calls = [{"id": "call_123", "type": "function"}]
        msg = Message(
            role=RoleType.ASSISTANT,
            content="Let me check that",
            tool_calls=tool_calls
        )
        assert msg.tool_calls == tool_calls
        assert msg.to_dict()["tool_calls"] == tool_calls

    def test_message_list_to_dict(self):
        """测试消息列表转换"""
        messages = [
            Message(role=RoleType.SYSTEM, content="You are a helpful assistant."),
            Message(role=RoleType.USER, content="Hello"),
        ]
        messages_dict = [m.to_dict() for m in messages]
        assert len(messages_dict) == 2
        assert messages_dict[0]["role"] == "system"
        assert messages_dict[1]["role"] == "user"

    def test_message_str_representation(self):
        """测试消息字符串表示"""
        msg = Message(role=RoleType.USER, content="Test message")
        str_repr = str(msg)
        assert "user" in str_repr
        assert "Test message" in str_repr

    def test_user_message_factory(self):
        """测试用户消息工厂方法"""
        msg = Message.user_message("Hello, world!")
        assert msg.role == RoleType.USER
        assert msg.content == "Hello, world!"

    def test_system_message_factory(self):
        """测试系统消息工厂方法"""
        msg = Message.system_message("You are a helpful assistant.")
        assert msg.role == RoleType.SYSTEM
        assert msg.content == "You are a helpful assistant."

    def test_assistant_message_factory(self):
        """测试助手消息工厂方法"""
        msg = Message.assistant_message("I can help you.")
        assert msg.role == RoleType.ASSISTANT
        assert msg.content == "I can help you."

    def test_tool_message_factory(self):
        """测试工具消息工厂方法"""
        msg = Message.tool_message("Tool result", tool_call_id="call_123")
        assert msg.role == RoleType.TOOL
        assert msg.content == "Tool result"
        assert msg.tool_call_id == "call_123"

    def test_message_with_base64_image(self):
        """测试带 base64 图片的消息"""
        msg = Message.user_message("What's in this image?", base64_image="data:image/png;base64,abc123")
        assert msg.base64_image == "data:image/png;base64,abc123"
