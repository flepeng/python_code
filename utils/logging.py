# -*- coding:utf-8 -*-
"""
    @Time  :
    @Author: Feng Lepeng
    @File  :
    @Desc  :
"""
import os
import logging.config


log_format_standard = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d][%(levelname)s][%(message)s]'
log_format_simple = '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]%(message)s'

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logfile_name = 'log/info.log'
logfile_path = os.path.join(basedir, logfile_name)

LOGGING_DIC = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': log_format_standard},
        'simple': {'format': log_format_simple},
    },
    'filters': {},
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'standard',
            'filename': logfile_path,
            'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
            'backupCount': 5,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'app': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
        __name__: {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,  # 向上（更高level的logger）传递
        },
    },
}

logging.config.dictConfig(LOGGING_DIC)
logger = logging.getLogger(__name__)
