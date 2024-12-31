# -*- coding:utf-8 -*-
"""
    @Time  : 2022/5/19  15:57
    @Author: Feng Lepeng
    @File  : ini_util.py
    @Desc  : ini 脚本
"""
import os
import configparser
import threading


class IniUtil(object):
    """
    ini配置文件是被configParser直接解析然后再加载的，如果只是修改配置文件，并不会改变已经加载的配置
    同时也说明 配置文件只会被加载一次
    """

    _instance_lock = threading.Lock()

    def __init__(self, file_name=r'../conf/config.ini'):
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

    # single mode，the config file must be control by the only one
    def __new__(cls, *arg, **kwargs):
        if not hasattr(IniUtil, "_instance"):
            with IniUtil._instance_lock:
                if not hasattr(IniUtil, "_instance"):
                    IniUtil._instance = object.__new__(cls)
        return IniUtil._instance

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


if __name__ == '__main__':
    iu = IniUtil()
    print(iu.get_config('MySQL', 'host'))