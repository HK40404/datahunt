from dataclasses import dataclass, field
from typing import Any


@dataclass
class SchemaMetadata:
    """数据库Schema向量检索的元数据结构"""
    table_name: str
    database: str
    type: str = "database_schema"
    # 字段类型信息: {column_name: data_type}
    column_types: dict[str, str] = field(default_factory=dict)
    # 索引信息: {key_name: {"columns": [col1, col2], "non_unique": bool}}
    indexes: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass
class QuestionMetadata:
    """问题骨架向量检索的元数据结构"""
    question_id: int
    db_id: str = "bird"
    type: str = "question_skeleton"
    # 原始问题
    original_question: str = ""
    # 证据/外部知识
    evidence: str = ""
    # 对应的 SQL
    sql: str = ""
    # 骨架中提取的数据库字面量
    database_literals: list[str] = field(default_factory=list)
