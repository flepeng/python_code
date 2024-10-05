# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/29  11:29
    @Author: Feng Lepeng
    @File  : alert_file_or_dir_name.py
    @Desc  : 更新文件名，把目录名字中的 、 更新为 -
"""
import os
import re


def alert_file_name(dir_name: str = None):
    """
    更新文件名，把目录名字中的 、 更新为 -
    :param dir_name: 需要更新的目录
    :return: None
    """

    for root, dirs, files in os.walk(dir_name):
        for d in dirs:
            # if d.find("、") != -1:
            ret = re.match("\d+、", d)
            if ret:
                print(d, ret.group(), str(ret.group()).replace("、", "-"))
                print(os.path.join(root, d.replace(ret.group(), str(ret.group()).replace("、", "-"))))
                os.rename(
                    os.path.join(root, d),
                    os.path.join(root,d.replace(ret.group(), str(ret.group()).replace("、", "-"))))
        # break


if __name__ == '__main__':
    alert_file_name("D:\\")
