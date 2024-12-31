# -*- coding:utf-8 -*-
"""
    @Time  : 2022/5/19  15:57
    @Author: Feng Lepeng
    @File  : 
    @Desc  : 
"""

import os
from src.util.ini_util import IniUtil


iu = IniUtil()


class Config:
    DEBUG = True
    ENV_NAME = 'Default'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # 自动 commit 提交到数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    DINGTALK_AGENT_ID = iu.get_config(ENV_NAME, 'dingtalk_agent_id')
    DINGTALK_APP_KEY = iu.get_config(ENV_NAME, 'dingtalk_app_key')
    DINGTALK_APP_SECRET = iu.get_config(ENV_NAME, 'dingtalk_app_secret')
    MYSQL_HOST = iu.get_config(ENV_NAME, 'mysql_host')
    MYSQL_USER = iu.get_config(ENV_NAME, 'mysql_user')
    MYSQL_PASSWD = iu.get_config(ENV_NAME, 'mysql_passwd')
    MYSQL_DB = iu.get_config(ENV_NAME, 'mysql_db')
    DINGTALK_APP_SECRET = iu.get_config(ENV_NAME, 'dingtalk_app_secret')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWD}@{MYSQL_HOST}:3306/{MYSQL_DB}"


class DevelopmentConfig(Config):
    """
    以开发模式的配置运行,并开启debug模式
    """
    DEBUG = True
    ENV_NAME = 'Development'


class TestingConfig(Config):
    """
    以开发模式的配置运行,并开启debug模式
    """
    DEBUG = True
    ENV_NAME = 'Testing'


class ProductionConfig(Config):
    """
    以生产模式的配置运行，关闭debug模式
    """
    DEBUG = False
    ENV_NAME = 'Production'


# 环境变量 ITINFO_ENV 两个参数 Development（开发）， Production（生产）, Testing（测试）
if os.environ.get('ENV') == "Development":
    conf = DevelopmentConfig()
elif os.environ.get('ENV') == "Production":
    conf = ProductionConfig()
elif os.environ.get('ENV') == "Testing":
    conf = TestingConfig()
else:
    conf = DevelopmentConfig()


if __name__ == '__main__':
    config = TestingConfig()
    print(config)
