# ========== prompt.yaml 配置结构 ==========
from pydantic import BaseModel


class ReactPrompt(BaseModel):
    system_prompt: str = ""
    next_step_prompt: str = ""


class QueryRewritterPrompt(BaseModel):
    system: str = ""
    user: str = ""


class SchemaRerankPrompt(BaseModel):
    system: str = ""
    user: str = ""


class SQLGeneratePrompt(BaseModel):
    system: str = ""
    user: str = ""
    final_prompt: str = ""


class SQLFixPrompt(BaseModel):
    system: str = ""
    system_notool: str = ""
    user: str = ""
    final_prompt: str = ""


class QuestionMaskPrompt(BaseModel):
    system: str = ""
    user: str = ""


class SQLSummaryPrompt(BaseModel):
    system: str = ""
    user: str = ""


class Prompt(BaseModel):
    react: ReactPrompt = ReactPrompt()
    query_rewritter: QueryRewritterPrompt = QueryRewritterPrompt()
    schema_rerank: SchemaRerankPrompt = SchemaRerankPrompt()
    sql_generate: SQLGeneratePrompt = SQLGeneratePrompt()
    sql_fix: SQLFixPrompt = SQLFixPrompt()
    question_mask: QuestionMaskPrompt = QuestionMaskPrompt()
    sql_summary: SQLSummaryPrompt = SQLSummaryPrompt()
