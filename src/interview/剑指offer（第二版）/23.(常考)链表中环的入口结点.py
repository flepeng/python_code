# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 17:48
    @File   : 23.(常考)链表中环的入口结点.py
    @Desc   : https://leetcode.cn/problems/linked-list-cycle-ii
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def detectCycle(self, head: [ListNode]) -> [ListNode]:
        slow = quick = head

        while quick:
            if quick.next:
                quick = quick.next
            else:
                return None
            if quick.next:
                quick = quick.next
            else:
                return None
            slow = slow.next
            if slow == quick:
                post = head  # 慢指针再从头走
                while slow != post:  # 两个指针都是每次一步直到相遇
                    slow = slow.next
                    post = post.next
                return post  # 相遇的地方即是环的入口

"""
q: a + on + c  = 2 (a + om + c) = 2a + 2om + c
s: a + om + c 
s + a 
"""