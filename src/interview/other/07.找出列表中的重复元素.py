# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 17:48
    @File   : 07.找出列表中的重复元素.py
    @Desc   :   列表中有 `1000000` 个元素，取值范围是 `[1000, 10000)`，设计一个函数找出列表中的重复元素。
"""


def find_dup(items: list):
    dups = [0] * 9000
    for item in items:
        dups[item - 1000] += 1
    for idx, val in enumerate(dups):
        if val > 1:
            yield idx + 1000
