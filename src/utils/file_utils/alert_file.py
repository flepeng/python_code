# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/29  11:29
    @Author: Feng Lepeng
    @File  : alert_file.py
    @Desc  : 将文件中替换之后的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
"""
import os


def alter(file, old_str, new_str):
    """
    将文件中替换之后的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
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
