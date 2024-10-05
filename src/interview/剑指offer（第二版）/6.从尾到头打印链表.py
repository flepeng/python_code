# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/2 20:08
    @File   : 6.从尾到头打印链表.py
    @Desc   : 输入一个链表，按链表从尾到头的顺序返回一个ArrayList。
              牛客: https://www.nowcoder.com/practice/d0267f7f55b3412ba93bd35cfa8e8035
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    # 返回从尾部到头部的列表值序列，例如[1,2,3]
    def printListFromTailToHead(self, head):
        res = []
        while head:
            res.append(head.val)
            head = head.next
        return res[::-1]


class Solution2:
    def printListReversingly(self, head):
        res = []

        def helper(p):
            if p:
                helper(p.next)
                res.append(p.val)

        helper(head)
        return res
