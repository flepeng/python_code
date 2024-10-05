# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/10 18:54
    @File   : 32.(常考)从上往下打印二叉树.py
    @Desc   : https://leetcode.cn/problems/binary-tree-level-order-traversal/
              https://www.nowcoder.com/practice/7fe2212963db4790b57431d9ed259701
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: [TreeNode]) -> list[list[int]]:
        if not root:
            return []
        tmp = [root]

        ret = [[root.val]]
        while tmp:
            tmp_next = []
            for i in tmp:
                if i.left:
                    tmp_next.append(i.left)
                if i.right:
                    tmp_next.append(i.right)
            tmp = tmp_next
            if tmp_next:
                ret.append([i.val for i in tmp_next])
            print(ret)
        return ret


def func():
    if not head.val:
        return
    tmp = [head]
    tmp_1 = []
    while tmp:
        for i in tmp:
            print(i.val)
            if i.left.val:
                tmp_l.append(i.left)
            if i.right.val:
                tmp_1.append(i.right)
        tmp = tmp_1
        tmp_1 = []


def func1():
    if not head.val:
        return
    tmp_list = [head]
    tmp_i = 0
    tmp_len = 1
    while True:
        for i in range(tmp_i, tmp_len - 1):
            print(tmp_list[i])
            if tmp_list[i].left.val:
                tmp_list.append(tmp_list[i].left)
            if tmp_list[i].right.val:
                tmp_list.append(tmp_list[i].right)
        if i == len(tmp_list):
            break
        tmp_i = i + 1
        tmp_len = len(tmp_list)


