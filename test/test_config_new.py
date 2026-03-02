"""
Config 模块测试

测试配置加载和管理功能
"""

import os
import pytest
from dotenv import load_dotenv

from config import DATAHUNT_CONFIG, Config, PROJECT_LOGGER_NAME

# 加载环境变量
load_dotenv(dotenv_path="config/.env")


class TestConfig:
    """Config 模块测试类"""

    def test_config_loading(self):
        """测试配置加载"""
        assert DATAHUNT_CONFIG is not None
        assert isinstance(DATAHUNT_CONFIG, Config)

    def test_logger_name(self):
        """测试日志名称定义"""
        assert PROJECT_LOGGER_NAME == "datahunt"
        assert isinstance(PROJECT_LOGGER_NAME, str)

    def test_config_has_openai(self):
        """测试配置包含 OPENAI 相关配置"""
        assert hasattr(DATAHUNT_CONFIG, "OPENAI_API_KEY")
        assert DATAHUNT_CONFIG.OPENAI_API_KEY is not None
        assert isinstance(DATAHUNT_CONFIG.OPENAI_API_KEY, str)

    def test_config_has_model(self):
        """测试配置包含模型配置"""
        assert hasattr(DATAHUNT_CONFIG, "OPENAI_MODEL")
        assert DATAHUNT_CONFIG.OPENAI_MODEL is not None
        assert isinstance(DATAHUNT_CONFIG.OPENAI_MODEL, str)

    def test_config_has_langsmith(self):
        """测试配置包含 LangSmith 配置"""
        assert hasattr(DATAHUNT_CONFIG, "LANGSMITH_API_KEY")
        assert DATAHUNT_CONFIG.LANGSMITH_API_KEY is not None

    def test_config_has_collection(self):
        """测试配置包含向量库 collection 配置"""
        assert hasattr(DATAHUNT_CONFIG, "SCHEMA_COLLECTION")
        assert DATAHUNT_CONFIG.SCHEMA_COLLECTION is not None

    def test_config_serialization(self):
        """测试配置序列化"""
        config_dict = DATAHUNT_CONFIG.model_dump()
        assert isinstance(config_dict, dict)
        assert "OPENAI_API_KEY" in config_dict
        assert "OPENAI_MODEL" in config_dict

    def test_config_environment_override(self):
        """测试环境变量覆盖"""
        # 设置测试环境变量
        os.environ["OPENAI_MODEL"] = "test-model"
        try:
            # 重新加载配置
            config = Config()
            # 验证环境变量被正确读取
            assert config.OPENAI_MODEL == "test-model"
        finally:
            # 恢复环境变量
            del os.environ["OPENAI_MODEL"]

    def test_root_dir(self):
        """测试根目录配置"""
        assert hasattr(DATAHUNT_CONFIG, "ROOT_DIR")
        assert DATAHUNT_CONFIG.ROOT_DIR is not None

    def test_config_dir(self):
        """测试配置目录配置"""
        assert hasattr(DATAHUNT_CONFIG, "CONFIG_DIR")
        assert DATAHUNT_CONFIG.CONFIG_DIR is not None
