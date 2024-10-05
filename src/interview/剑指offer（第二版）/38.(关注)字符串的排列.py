# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/11 17:22
    @File   : 38.(关注)字符串的排列.py
    @Desc   :   输入一组数字（可能包含重复数字），输出其所有的排列方式。
                https://leetcode.cn/problems/permutations/
"""


class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        tmp = []
        ret = []
        def inner(nums):
            for num in nums:
                others = nums[:]
                others.remove(num)
                tmp.append(num)
                print(111, tmp, others)
                if others:
                    inner(others)
                else:
                    ret.append(tmp[:])
                tmp.pop()

        inner(nums)
        return ret


class Solution2:
    def permutation(self, nums):
        perms = [[]]
        for n in nums:
            tmp = []
            # perms = [
            #     p[:i] + [n] + p[i:]
            #     for p in perms
            #     for i in range((p+[n]).index(n)+1)]
            for p in perms:
                for i in range((p+[n]).index(n)+1):
                    tmp.append(p[:i] + [n] + p[i:])
            perms = tmp
        return perms