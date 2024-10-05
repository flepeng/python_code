# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/5 14:29
    @File   : 02.无重复有序数组转换成最小高度的二叉搜索树.py
    @Desc   : 无重复有序数组转换成最小高度的二叉搜索树，要求：
                A:二叉搜索树的严格定义及高度
                B:定义二叉树的节点
                C:实现有序数组转换成最小高度二叉搜索树
                D:准备充分的测试用例（最好能够运行）
"""


# encoding: utf-8
# a = input("please input a number:")
print("hello world")


class TreeNode():
    def __init__(self, val, left=None, right=None) -> None:
        self.val = val
        self.left = left
        self.right = right


head = TreeNode(0)


def func(sort_list):
    if not sort_list:
        return None
    list_len = len(sort_list)
    mid = list_len // 2
    left = func(sort_list[0: mid])
    right = func(sort_list[mid+1: ])
    node = TreeNode(sort_list[mid])
    node.left = left
    node.right = right
    return node


sort_list = [i for i in range(100)]
node = func(sort_list)
print(node.val)
print(node.left.val)
print(node.right.val)