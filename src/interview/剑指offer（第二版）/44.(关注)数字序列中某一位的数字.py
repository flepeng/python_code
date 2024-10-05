# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/12 18:00
    @File   : 44.(关注)数字序列中某一位的数字.py
    @Desc   :   https://leetcode.cn/problems/nth-digit/
"""


class Solution:
    def findNthDigit(self, n: int) -> int:
        n -= 1
        for i in range(1, 11):
            first = 10 ** (i - 1)
            num = 9 * first * i
            if n < num:
                print(i, n, n // i, n % i)
                return int(str(first + n // i)[n % i])

            n -= num
