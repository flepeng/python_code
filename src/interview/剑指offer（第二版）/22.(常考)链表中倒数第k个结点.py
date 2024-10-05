# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 17:31
    @File   : 22.(常考)链表中倒数第k个结点.py
    @Desc   : 输入一个链表，输出该链表中倒数第k个节点。
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def findKthToTail(self, head, k):
        if not head or k <= 0:
            return None
        fast = slow = head
        for _ in range(k):  # 快慢指针来走，之所以先判断是为了防止 k 等于链表长度的情况。
            if not fast: return None
            fast = fast.next
        while fast:
            fast, slow = fast.next, slow.next
        return slow
