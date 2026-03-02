from typing import Any

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

from data_types.message import Message, RoleType
from graph.graph import text_to_sql

limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


class MessageInput(BaseModel):
    """消息输入模型"""

    role: str = Field(..., description="消息角色: user, assistant, system")
    content: str = Field(..., description="消息内容")


class QueryRequest(BaseModel):
    """查询请求模型"""

    messages: list[MessageInput] = Field(..., description="对话历史消息列表")
    evidence: str = Field(default="", description="外部知识/证据")
    database: str = Field(default="bird", description="数据库名称")


class QueryResponse(BaseModel):
    """查询响应模型"""

    exec_result: list[dict[str, Any]] = Field(default_factory=list, description="SQL 执行结果")
    generated_sql: str = Field(default="", description="生成的 SQL")
    answer: str | None = Field(default=None, description="自然语言答案")


def _convert_messages(messages: list[MessageInput]) -> list[Message]:
    """将输入消息转换为 Message 对象"""
    result = []
    for msg in messages:
        role = RoleType(msg.role)
        result.append(Message(role=role, content=msg.content))
    return result


@router.post("/query", response_model=QueryResponse)
@limiter.limit("10/minute")
async def query(request: Request, body: QueryRequest) -> QueryResponse:
    """
    Text-to-SQL 查询接口

    接受消息列表，返回 SQL 执行结果和生成的 SQL。

    限流: 每分钟最多 10 次请求
    """
    # 转换消息格式
    messages = _convert_messages(body.messages)

    # 构建 State
    state = {
        "question": "",
        "messages": messages,
        "evidence": body.evidence,
        "database": body.database,
        "generated_sql": "",
        "matched_tables": [],
        "DDL": [],
        "exec_result": [],
        "exec_error": "",
        "validate_error": None,
        "review_result": True,
        "review_comment": "",
        "fix_count": 0,
    }

    # 调用 LangGraph 工作流
    result = await text_to_sql(state)

    # 只返回 exec_result 和 generated_sql
    return QueryResponse(
        exec_result=result.get("exec_result", []),
        generated_sql=result.get("generated_sql", ""),
        answer=result.get("answer"),
    )
