# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/3 20:47
    @File   : 10.斐波那契数列.py
    @Desc   : https://leetcode.cn/problems/fei-bo-na-qi-shu-lie-lcof/
"""


class Solution:
    def fib(self, n: int) -> int:
        if n == 0 :
            return 0
        if n == 1:
            return 1
        return self.fib(n-1) + self.fib(n-2)


class Solution1:
    def fib(self, n: int) -> int:
        MOD = 10 ** 9 + 7
        if n == 0:
            return 0
        if n == 1:
            return 1
        a = 0
        b = 1
        for _ in range(n-1):
            a, b = b, a+b
        return b % MOD