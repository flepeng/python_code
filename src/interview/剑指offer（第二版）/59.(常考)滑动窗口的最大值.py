# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/12 20:57
    @File   : 59.(常考)滑动窗口的最大值.py
    @Desc   :   https://www.nowcoder.com/practice/1624bc35a45c42c0bc17d17fa0cba788
"""


class Solution:
    def maxInWindows(self, num: list[int], size: int) -> list[int]:
        if size == 0:
            return []
        if len(num) < size:
            return []
        # write code here
        tmp_max = 0
        ret = []
        for i in range(1, size):
            if num[i] >= num[tmp_max]:
                tmp_max = i
        ret.append(num[tmp_max])
        for i in range(size, len(num)):
            if num[i] >= num[tmp_max]:
                tmp_max = i
            if tmp_max <= i - size:
                tmp_max = i - size + 1
                for j in range(i - size + 1, i):
                    if num[j] >= num[tmp_max]:
                        tmp_max = j

            ret.append(num[tmp_max])
        return ret
