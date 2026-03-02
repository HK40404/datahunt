"""
Config 模块

提供配置和日志初始化功能
"""

from config.config import Config
from config.log import PROJECT_LOGGER_NAME, setup_logging

DATAHUNT_CONFIG = Config()
# 初始化日志系统
setup_logging()

__all__ = ['DATAHUNT_CONFIG', 'PROJECT_LOGGER_NAME']
