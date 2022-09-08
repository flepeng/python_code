# -*- coding:utf-8 -*-
"""
    @Time  : 2022/5/19  15:57
    @Author: Feng Lepeng
    @File  :
    @Desc  :
"""
import os
import datetime
import configparser
import threading


class OPConfig(object):
    """
    ini配置文件是被configParser直接解析然后再加载的，如果只是修改配置文件，并不会改变已经加载的配置
    同时也说明 配置文件只会被加载一次
    """

    _instance_lock = threading.Lock()

    def __init__(self, file_name='D:\home\my_git\code\config.ini'):
        # file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__name__))), file_name)
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

    # single mode，the config file must be control by the only one
    def __new__(cls, *arg, **kwargs):
        if not hasattr(OPConfig, "_instance"):
            with OPConfig._instance_lock:
                if not hasattr(OPConfig, "_instance"):
                    OPConfig._instance = object.__new__(cls)
        return OPConfig._instance

    def get_config(self, section, k):
        return self.config.get(section, k)

    def get_section(self):
        return self.config.sections()

    def get_section_all_key(self, section):
        return self.config.options(section)

    def add_section(self, section):
        self.config.add_section(section)

    def update_k(self, section, k, v):
        # 更新相应的k，如果没有对应的k，会自动创建 k，判断k时不区分大小写。
        self.config.set(section, k, v)

    def remove_section(self, section):
        self.config.remove_section(section)

    def remove_k(self, section, k):
        self.config.remove_option(section, k)

    def save_config(self):
        with open(self.file_name, "w+") as f:
            self.config.write(f)


opc = OPConfig()


class Config:
    DEBUG = True
    ENV_NAME = 'Default'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    # 自动 commit 提交到数据库
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    def __init__(self):
        self.DINGTALK_AGENT_ID = opc.get_config(self.ENV_NAME, 'dingtalk_agent_id')
        self.DINGTALK_APP_KEY = opc.get_config(self.ENV_NAME, 'dingtalk_app_key')
        self.DINGTALK_APP_SECRET = opc.get_config(self.ENV_NAME, 'dingtalk_app_secret')
        self.MYSQL_HOST = opc.get_config(self.ENV_NAME, 'mysql_host')
        self.MYSQL_USER = opc.get_config(self.ENV_NAME, 'mysql_user')
        self.MYSQL_PASSWD = opc.get_config(self.ENV_NAME, 'mysql_passwd')
        self.MYSQL_DB = opc.get_config(self.ENV_NAME, 'mysql_db')
        self.DINGTALK_APP_SECRET = opc.get_config(self.ENV_NAME, 'dingtalk_app_secret')
        self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWD}@{self.MYSQL_HOST}:3306/{self.MYSQL_DB}"

        self.CMDB_MYSQL_HOST = opc.get_config("Default", 'cmdb_mysql_host')
        self.CMDB_MYSQL_USER = opc.get_config("Default", 'cmdb_mysql_user')
        self.CMDB_MYSQL_PASSWD = opc.get_config("Default", 'cmdb_mysql_passwd')
        self.CMDB_MYSQL_DB = opc.get_config("Default", 'cmdb_mysql_db')

        # sso 配置
        self.USE_SSO = False if opc.get_config(self.ENV_NAME, 'use_sso') == 'false' else True  # 是否使用 sso
        self.DEBUG_AS_USER = opc.get_config(self.ENV_NAME, 'debug_as_user')  # 不使用sso时，默认的登陆用户
        self.LOCAL_IP = opc.get_config(self.ENV_NAME, 'local_ip')
        self.SSO_LOGIN_CALLBACK_URL = "http://{}:{}/api/v1/auth/login_callback".format(self.LOCAL_IP, '8080')
        self.SSO_LOGOUT_CALLBACK_URL = "http://{}:{}/api/v1/auth/logout_callback".format(self.LOCAL_IP, '8080')
        self.SSO_CLIENT_ID = opc.get_config(self.ENV_NAME, 'sso_client_id')
        self.SSO_CLIENT_SECRET = opc.get_config(self.ENV_NAME, 'sso_client_secret')


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

    opc = OPConfig()
    print(opc.get_config('MySQL', 'host'))
