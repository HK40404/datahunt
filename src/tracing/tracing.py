"""
Trace 上下文管理

使用 ContextVar 实现全链路追踪，每次请求分配唯一 trace_id。
"""

import logging
import uuid
from contextvars import ContextVar

# ContextVar 存储当前请求的 trace_id
_trace_id_var: ContextVar[str | None] = ContextVar("trace_id", default=None)


def get_trace_id() -> str:
    """获取当前请求的 trace_id"""
    tid = _trace_id_var.get()
    if tid is None:
        # 如果没有设置，返回 placeholder
        return "N/A"
    return tid


def new_trace_id() -> str:
    """生成新的 trace_id 并设置为当前上下文"""
    tid = str(uuid.uuid4())[:8]  # 截取前8位，够用且短
    _trace_id_var.set(tid)
    return tid


def set_trace_id(trace_id: str) -> None:
    """手动设置 trace_id（用于测试或外部传入）"""
    _trace_id_var.set(trace_id)


class TraceLogFilter(logging.Filter):
    """日志过滤器，自动添加 trace_id 到每条日志"""

    def filter(self, record: logging.LogRecord) -> bool:
        # 从 ContextVar 获取 trace_id
        trace_id = get_trace_id()
        # 添加到 record，方便日志格式器使用
        record.trace_id = trace_id
        return True
