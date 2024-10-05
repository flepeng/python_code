# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 17:04
    @File   : 04.给两个字符串 s 和 t，判断 t 是否为 s 的重新排列后组成的单词.py
    @Desc   :
                *   `ns = "anagram", t = "nagaram", return true.`
                *   `ns = "rat", t = "car", return false.`
"""


class Solution:
    def isAnagram(self, s, t):
        dict1 = {}   # 用字典来维护字符的数量
        dict2 = {}
        for ch in s:
            dict1[ch] = dict1.get(ch, 0) + 1   # 没有就新建，有就加1
        for ch in t:
            dict2[ch] = dict2.get(ch, 0) + 1
        return dict1 == dict2