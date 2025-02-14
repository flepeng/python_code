# -*- coding:utf-8 -*-
"""
    @Time  :
    @Author: Feng Lepeng
    @File  : logging_util.py
    @Desc  : logging 脚本
"""

import os
import logging.config

WRITE_FILE = os.environ.get("ENV") in ["Production", "Testing"]


def get_logger():

    standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'
    simple_format = '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]%(message)s'

    basedir = os.path.dirname(os.path.dirname(__file__))

    LOGGING_DICT = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": standard_format},
            "simple": {"format": simple_format},
        },
        "filters": {},
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "simple"
            },
            "console_werkzeug": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
            },
            "file_werkzeug": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(basedir, "logs/sem.log"),
                "maxBytes": 1024 * 1024 * 100,  # 日志大小 100M
                "backupCount": 5,
                "encoding": "utf-8",
            },
            "file_cron": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(basedir, "logs/cron.log"),
                "maxBytes": 1024 * 1024 * 100,  # 日志大小 100M
                "backupCount": 5,
                "encoding": "utf-8",
                "formatter": "simple"
            },
            "file_app": {
                "level": "DEBUG",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": os.path.join(basedir, "logs/app.log"),
                "maxBytes": 1024 * 1024 * 100,  # 日志大小 100M
                "backupCount": 5,
                "encoding": "utf-8",
                "formatter": "simple"
            },
        },
        "loggers": {
            "app_cron": {
                "handlers": ["file_cron"] if WRITE_FILE else ["console", "file_cron"],
                "level": "DEBUG",
                "propagate": True,  # 向上（更高level的logger）传递
            },
            # apscheduler.scheduler 定时任务
            "apscheduler.scheduler": {
                "handlers": ["file_cron"] if WRITE_FILE else ["console", "file_cron"],
                "level": "DEBUG",
                "propagate": True,  # 向上（更高level的logger）传递
            },
            # flask 的 配置
            "werkzeug": {
                "handlers": ["file_werkzeug"] if WRITE_FILE else ["console_werkzeug", "file_werkzeug"],
                "level": "DEBUG",
                "propagate": True,  # 向上（更高level的logger）传递
            },
            __name__: {
                "handlers": ["file_app"] if WRITE_FILE else ["console", "file_app"],
                "level": "DEBUG",
                "propagate": True,  # 向上（更高level的logger）传递
            },
        },
    }

    logging.config.dictConfig(LOGGING_DICT)
    logging.getLogger("requests").setLevel(logging.WARNING)  # 把 request 模块的log 级别设置为 warning
    logging.getLogger("urllib3").setLevel(logging.WARNING)   # 把 urllib3 模块的log 级别设置为 warning

    if os.environ.get("cron"):
        logger = logging.getLogger("app_cron")
    else:
        logger = logging.getLogger(__name__)
