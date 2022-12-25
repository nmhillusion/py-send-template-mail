import logging
from datetime import datetime
from enum import Enum

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QListWidget, QListWidgetItem

MAX_LOG_SIZE = 50


class LoggingLevelConfig:
    def __init__(self, name: str, colorName: str):
        self.name = name
        self.colorName = colorName


class LoggingLevel(Enum):
    ERROR: LoggingLevelConfig = LoggingLevelConfig("ERROR", "red")
    WARNING: LoggingLevelConfig = LoggingLevelConfig("WARN", "orange")
    WARN: LoggingLevelConfig = LoggingLevelConfig("WARN", "orange")
    INFO: LoggingLevelConfig = LoggingLevelConfig("INFO", "#3366ff")
    DEBUG: LoggingLevelConfig = LoggingLevelConfig("DEBUG", "gray")


def apply_widget(widget_: QListWidget):
    global __widget
    __widget = widget_


def debug(message_: str):
    __do_logging__(message_, LoggingLevel.DEBUG)


def info(message_: str):
    __do_logging__(message_, LoggingLevel.INFO)


def warning(message_: str):
    __do_logging__(message_, LoggingLevel.WARNING)


def error(message_: str):
    __do_logging__(message_, LoggingLevel.ERROR)


def __build_logging_message__(message_: str, level_: LoggingLevel):
    return f"{datetime.today().now().strftime('%Y-%m-%dT%H:%M:%S')} - {level_.value.name} : {message_}"


def __build_logging_message_list_item__(message_: str, level_: LoggingLevel):
    logging_item_ = QListWidgetItem(message_)
    logging_item_.setForeground(QColor(level_.value.colorName))
    logging_item_.setFont(QFont("Consolas"))

    return logging_item_


def __do_logging__(message_: str, level_: LoggingLevel):
    logging_message_ = __build_logging_message__(message_, level_)
    logging_message_item_ = __build_logging_message_list_item__(logging_message_, level_)

    logging.info(logging_message_)
    if __widget is not None:
        __widget.addItem(logging_message_item_)

        while MAX_LOG_SIZE < __widget.count():
            __widget.takeItem(0)

        __widget.scrollToBottom()
