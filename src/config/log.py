import logging
import sys
from pathlib import Path

# 标记是否已经初始化过日志系统
_logging_initialized = False

# 设置项目的parent logger
PROJECT_LOGGER_NAME = "datahunt"


class ShortNameFormatter(logging.Formatter):
    """
    自定义格式化器，只显示当前logger名（叶子节点），不显示父logger名

    例如：
    - datahunt.module.submodule -> submodule
    - datahunt.utils -> utils
    """

    def format(self, record: logging.LogRecord) -> str:
        # 只保留最后一个点之后的部分作为logger名
        if record.name and "." in record.name:
            record.name = record.name.split(".")[-1]

        # 从 ContextVar 获取 trace_id
        from tracing.tracing import get_trace_id
        trace_id = get_trace_id()
        if not trace_id or trace_id == 'N/A':
            record.trace_id = '-'
        else:
            record.trace_id = trace_id

        return super().format(record)

def setup_logging():
    """
    初始化日志系统

    该函数只会执行一次，即使被多次调用也不会重复初始化。
    """
    global _logging_initialized

    # 如果已经初始化过，直接返回
    if _logging_initialized:
        return

    # 延迟导入避免循环导入
    from config import DATAHUNT_CONFIG

    level = DATAHUNT_CONFIG.LOG_LEVEL
    console_log_level = getattr(DATAHUNT_CONFIG, "CONSOLE_LOG_LEVEL", "DEBUG")
    third_party_log_level = DATAHUNT_CONFIG.THIRD_PARTY_LOG_LEVEL
    log_to_file = DATAHUNT_CONFIG.LOG_TO_FILE
    log_dir = DATAHUNT_CONFIG.LOG_DIR
    log_format = DATAHUNT_CONFIG.LOG_FORMAT
    log_date_format = getattr(DATAHUNT_CONFIG, "LOG_DATE_FORMAT", None)

    # 创建根 logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, third_party_log_level.upper(), logging.INFO))

    # 解析日志等级
    numeric_level = getattr(logging, level.upper(), logging.INFO)  # 日志级别
    console_numeric_level = getattr(logging, console_log_level.upper(), logging.DEBUG)  # 控制台日志级别
    # 为项目模块设置日志级别（使用文件日志级别，因为文件记录更详细）
    logging.getLogger(PROJECT_LOGGER_NAME).setLevel(numeric_level)

    # 清除已有的 handlers（避免重复添加）
    root_logger.handlers.clear()

    # 创建格式化器（使用自定义格式化器，只显示当前logger名）
    formatter = ShortNameFormatter(log_format, datefmt=log_date_format)

    # 添加控制台 handler（使用 FILE_LOG_LEVEL）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_numeric_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 如果需要输出到文件
    if log_to_file:
        log_path = Path(log_dir)
        log_path.mkdir(parents=True, exist_ok=True)

        # 创建文件格式化器（详细格式，使用自定义格式化器）
        file_formatter = ShortNameFormatter(log_format, datefmt=log_date_format)

        file_handler = logging.FileHandler(
            log_path / "app.log",
            encoding="utf-8",
        )
        file_handler.setLevel(numeric_level)  # 使用 LOG_LEVEL
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

    # 标记为已初始化
    _logging_initialized = True
