from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

from context.prompt import Prompt

root_path = Path(__file__).resolve().parent.parent.parent
config_path = root_path / 'config'

class YamlConfigSource(PydanticBaseSettingsSource):

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:
        return None, field_name, False

    def __call__(self) -> dict[str, Any]:
        global config_path

        if not config_path.exists():
            return {}

        merged_config = {}

        # 递归扫描 config 目录下的所有 yaml 文件
        yaml_files = list(config_path.rglob("*.yaml")) + list(config_path.rglob("*.yml"))

        for yaml_file in sorted(yaml_files):
            try:
                with open(yaml_file, encoding="utf-8") as f:
                    content = yaml.safe_load(f) or {}

                # 计算相对路径，用于构建配置键名
                relative_path = yaml_file.relative_to(config_path)
                # 移除文件扩展名
                path_parts = list(relative_path.parts[:-1]) + [relative_path.stem]

                # 如果是 config.yaml，直接合并到根级别
                if path_parts == ["config"]:
                    merged_config.update(content)
                else:
                    # 否则创建嵌套结构，例如 prompts/react.yaml -> prompts.react
                    current = merged_config
                    for part in path_parts[:-1]:
                        if part not in current:
                            current[part] = {}
                        current = current[part]
                    current[path_parts[-1]] = content
            except Exception as e:
                # 忽略无法解析的文件
                print(f"Warning: Failed to load {yaml_file}: {e}")
                continue

        return merged_config

class Config(BaseSettings):
    CONFIG_DIR: Path = config_path
    ROOT_DIR: Path = root_path

    OPENAI_BASE_URL: str
    OPENAI_MODEL: str
    OPENAI_API_KEY: str

    GEMINI_MODEL: str
    GEMINI_API_KEY: str

    SQL_API_KEY: str
    SQL_BASE_URL: str
    SQL_MODEL: str

    SKELETON_EXTRACTOR_API_KEY: str
    SKELETON_EXTRACTOR_BASE_URL: str
    SKELETON_EXTRACTOR_MODEL: str

    REWRITE_API_KEY: str
    REWRITE_BASE_URL: str
    REWRITE_MODEL: str

    # question skeleton collection 配置
    SKELETON_COLLECTION: str = "question_skeleton"
    SCHEMA_COLLECTION: str = "bird"

    # langsmith
    LANGSMITH_API_KEY: str
    LANGSMITH_BASE_URL: str = "https://api.smith.langchain.com"
    LANGSMITH_PROJECT_NAME: str

    # LLM 全局配置
    LLM_MAX_RETRIES: int = 2  # LLM API 调用最大重试次数，默认 2 次

    # vectordb
    RAW_MILVUS_URI: str = Field(default="./store/milvus.db", alias="MILVUS_URI")
    MILVUS_TOKEN: str | None = None
    @property
    def MILVUS_URI(self) -> str:
        """返回 root_dir + 原本的 milvus_uri 值"""
        # 如果是 URI（以 http:// 或 https:// 开头），直接返回
        if self.RAW_MILVUS_URI.startswith(("http://", "https://")):
            return self.RAW_MILVUS_URI
        # 如果原本的值已经是绝对路径，直接返回
        if Path(self.RAW_MILVUS_URI).is_absolute():
            return self.RAW_MILVUS_URI
        # 否则返回 root_dir + 原本的值
        return str(self.ROOT_DIR / self.RAW_MILVUS_URI)

    # logging config
    LOG_LEVEL: str = "DEBUG"
    LOG_DIR: str = "logs"
    LOG_TO_FILE: bool = True
    LOG_FORMAT: str = "%(asctime)s - %(trace_id)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DATE_FORMAT: str = "%H:%M:%S"  # 时间格式：只显示时:分:秒，不包含日期和毫秒
    CONSOLE_LOG_LEVEL: str = "INFO"  # 控制台日志级别，默认 DEBUG
    THIRD_PARTY_LOG_LEVEL: str = "WARNING"

    # prompt config (from config/prompt.yaml)
    PROMPT: Prompt = Field(default=Prompt(), alias="prompt")

    model_config = SettingsConfigDict(
        env_file= config_path / ".env",
        extra="ignore",  # 忽略未定义的字段
        populate_by_name=True  # 允许使用字段名和别名
    )

    def get_nested(self, path: str, default: Any = None) -> Any:
        """
        获取嵌套配置值

        Args:
            path: 点分隔的路径，例如 "prompt.react.prompt"
            default: 如果路径不存在，返回的默认值

        Returns:
            配置值或默认值

        Example:
            config.get_nested("prompt.react.prompt")
        """
        keys = path.split(".")
        value = self

        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            elif hasattr(value, key):
                value = getattr(value, key)
            else:
                return default

            if value is None:
                return default

        return value

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        定义配置加载的优先级（从上到下，优先级依次降低）
        """
        return (
            init_settings,          # 1. 代码中直接初始化的参数 (Settings(debug=True))
            env_settings,           # 2. 系统环境变量
            dotenv_settings,        # 3. .env 文件
            YamlConfigSource(settings_cls), # 4. config.yaml (自定义源)
            file_secret_settings,   # 5. Docker secrets 等
        )
