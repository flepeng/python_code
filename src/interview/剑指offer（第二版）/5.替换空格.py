# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/2 20:08
    @File  :
    @Desc  : 请实现一个函数，将一个字符串中的每个空格替换成“%20”。例如，当字符串为 We Are Happy .则经过替换之后的字符串为 We%20Are%20Happy  。
"""


class Solution:
    # s 源字符串
    def replace_space(self, s):
        res = []
        for i in s:
            if i == ' ':
                res.extend(['%', '2', '0'])
            else:
                res.append(i)
        return ''.join(res)