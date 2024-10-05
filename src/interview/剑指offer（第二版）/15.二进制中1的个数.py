# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 11:25
    @File   : 15.二进制中1的个数.py
    @Desc   : https://leetcode.cn/problems/number-of-1-bits/
"""
class Solution:
    def hammingWeight(self, n: int) -> int:
        n_bin = bin(n)
        count = 0
        for i in n_bin:
            print(i)
            if i == "1":
                count += 1
        print(count)
        return count


class Solution2:
    def hammingWeight(self, n: int) -> int:
        count = 0
        for _ in range(32):
            count += (n & 1 == 1)
            n >>= 1
        return count