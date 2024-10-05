# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 11:41
    @File   : 16.(关注)数值的整数次方.py
    @Desc   : https://leetcode.cn/problems/powx-n/
"""


class Solution:
    def myPow(self, x: float, n: int) -> float:
        exp = abs(n)
        r = 1
        while exp:
            if exp & 1:
                r *= x
            x *= x
            exp >>= 1
        return r if n >= 0 else 1/r