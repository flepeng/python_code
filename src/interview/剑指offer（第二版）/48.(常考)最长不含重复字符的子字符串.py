# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/12 18:46
    @File   : 48.(常考)最长不含重复字符的子字符串.py
    @Desc   :   https://leetcode.cn/problems/longest-substring-without-repeating-characters/
"""


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start, end = 0, 0
        tmp_dict = {}
        max_str = 0
        for i, num in enumerate(s):
            if num not in s[start: end]:
                tmp_dict[num] = i
            else:
                start = tmp_dict[num] + 1
                tmp_dict[num] = i
            end = i + 1
            max_str = max(end - start, max_str)
        return max_str
