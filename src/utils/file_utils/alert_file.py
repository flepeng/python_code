# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/29  11:29
    @Author: Feng Lepeng
    @File  : alert_file.py
    @Desc  :
"""
import os


def alter(file: str = None, old_str: str = None, new_str: str = None):
    """
    遍历文件中的行并进行替换，然后写到一个新文件中，然后将原文件删除，新文件改为原来文件的名字
    :param file: 文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)


if __name__ == '__main__':
    pass
