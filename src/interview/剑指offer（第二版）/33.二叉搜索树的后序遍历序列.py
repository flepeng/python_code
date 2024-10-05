# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/10 19:31
    @File   : 33.二叉搜索树的后序遍历序列.py
    @Desc   :   判断给定的整数数组是不是二叉搜索树的后序遍历序列
"""


def is_post_order(order):
    root = order[-1]
    for i, num in enumerate(order):
        if num > root:
            break
    for i in range(i, len(root)):
        if order[i] < root:
            return False
    return is_post_order(order[0: i]) and is_post_order(order[i + 1:])
