# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/12 20:58
    @File   : 57.(关注)和为S的连续正数序列.py
    @Desc   :   https://www.nowcoder.com/practice/c451a3fd84b64cb19485dad758a55ebe?
"""


class Solution:
    def FindContinuousSequence(self, sum: int) -> list[list[int]]:
        # write code here
        l, r = 1, 2
        tmp_sum = 1 + 2
        ret = []
        while l < sum - 1 and r < sum:
            while tmp_sum < sum:
                r += 1
                tmp_sum = tmp_sum + r
            while tmp_sum > sum:
                tmp_sum = tmp_sum - l
                l += 1
            if tmp_sum == sum:
                ret.append([i for i in range(l, r + 1)])
                tmp_sum = tmp_sum - l
                l += 1
        return ret
