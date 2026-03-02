"""
配置模块测试
测试 Config 类的核心功能：
1. 基本配置加载（从环境变量/.env）
2. YAML 配置加载（从 config/ 目录）
3. 嵌套配置访问（get_nested 方法和属性访问）
4. 配置优先级验证
"""

from pathlib import Path

from config.config import Config, YamlConfigSource
from config.config_type import Prompt, ReactPrompt


def test_config_basic_loading():
    """测试基本配置加载"""
    # Config 应该能从环境变量或 .env 加载必要配置
    config = Config()
    
    # 验证必要字段存在
    assert hasattr(config, 'openai_api_key')
    assert hasattr(config, 'openai_base_url')
    assert hasattr(config, 'model')
    
    # 验证默认值
    assert config.vector_db_dir == "./store/"
    assert config.log_level == "INFO"
    assert config.log_dir == "logs"
    assert config.log_to_file == False
    assert config.third_party_log_level == "WARNING"
    
    print(f"openai_base_url: {config.OPENAI_BASE_URL}")
    print(f"model: {config.OPENAI_MODEL}")
    print(f"vector_db_dir: {config.vector_db_dir}")


def test_yaml_config_source():
    """测试 YAML 配置源加载"""
    # 创建 YamlConfigSource 实例
    source = YamlConfigSource(Config)
    
    # 调用获取配置
    config_dict = source()
    
    # 验证返回类型
    assert isinstance(config_dict, dict)
    
    # 如果 config/ 目录存在，应该能加载到配置
    config_dir = Path("config")
    if config_dir.exists():
        print(f"加载的配置: {config_dict}")
        
        # 验证 prompt.yaml 被正确加载为 prompt 键
        if (config_dir / "prompt.yaml").exists():
            assert "prompt" in config_dict
            assert "react" in config_dict["prompt"]
            print(f"prompt 配置: {config_dict['prompt']}")


def test_prompt_config_structure():
    """测试 prompt 配置结构"""
    config = Config()
    
    # 验证 prompt 字段存在且类型正确
    assert hasattr(config, 'prompt')
    assert isinstance(config.PROMPT, Prompt)
    
    # 验证嵌套结构
    assert hasattr(config.PROMPT, 'react')
    assert isinstance(config.PROMPT.react, ReactPrompt)
    
    # 验证 ReactPrompt 字段
    assert hasattr(config.PROMPT.react, 'system_prompt')
    assert hasattr(config.PROMPT.react, 'next_step_prompt')
    
    print(f"prompt.react.prompt: {config.PROMPT.react.system_prompt}")
    print(f"prompt.react.next_step_prompt: {config.PROMPT.react.next_step_prompt}")


def test_get_nested():
    """测试 get_nested 方法"""
    config = Config()
    
    # 测试有效路径
    react_prompt = config.get_nested("prompt.react.system_prompt")
    assert react_prompt is not None or react_prompt == ''
    
    next_step = config.get_nested("prompt.react.next_step_prompt")
    assert next_step is not None or next_step == ''
    
    # 测试无效路径，应返回默认值
    invalid = config.get_nested("invalid.path.here", default="default_value")
    assert invalid == "default_value"
    
    # 测试部分有效路径
    react = config.get_nested("prompt.react")
    assert isinstance(react, ReactPrompt)
    
    print(f"get_nested('prompt.react.system_prompt'): {react_prompt}")
    print(f"get_nested('invalid.path.here', default='default_value'): {invalid}")


def test_config_attribute_access():
    """测试通过属性直接访问配置"""
    config = Config()
    
    # 直接属性访问（类型安全方式）
    prompt_value = config.PROMPT.react.system_prompt
    next_step_value = config.PROMPT.react.next_step_prompt
    
    # 验证返回类型
    assert isinstance(prompt_value, str)
    assert isinstance(next_step_value, str)
    
    print(f"config.prompt.react.prompt: {prompt_value}")
    print(f"config.prompt.react.next_step_prompt: {next_step_value}")


def test_extra_fields_ignored():
    """测试未定义的额外字段被忽略"""
    # 使用额外的初始化参数，应该被忽略（extra="ignore"）
    config = Config(
        unknown_field="should_be_ignored"  # type: ignore
    )
    
    # 验证未定义字段不存在
    assert not hasattr(config, 'unknown_field')
    
    print("额外字段已被正确忽略")


def test_datahunt_config_singleton():
    """测试全局配置实例"""
    from config import DATAHUNT_CONFIG
    
    # 验证全局实例存在
    assert DATAHUNT_CONFIG is not None
    assert isinstance(DATAHUNT_CONFIG, Config)
    
    # 验证可以访问配置
    assert hasattr(DATAHUNT_CONFIG, 'openai_api_key')
    
    print(f"DATAHUNT_CONFIG.model: {DATAHUNT_CONFIG.OPENAI_MODEL}")

