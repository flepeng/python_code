# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 17:16
    @File   : 21.(关注)调整数组顺序使奇数位于偶数前面.py
    @Desc   : 输入一个整数数组，实现一个函数来调整该数组中数字的顺序，
              使得所有的奇数位于数组的前半部分，所有的偶数位于数组的后半部分，
              并保证奇数和奇数，偶数和偶数之间的相对位置不变。
"""


class Solution:
    def reOrderArray(self, array):
        if not array:
            return array

        array_len = len(array)
        l = 0
        r = array_len
        while l < r:
            while array[l] % 2 == 1 and l < r:
                l += 1

            while array[r] % 2 == 0 and l < r:
                r -= 1

            array[l], array[r] = array[r], array[l]


class Solution1:
    def reOrderArray(self, array):
        # write code here
        qian = []
        hou = []
        for i in array:
            qian.append(i) if i % 2 == 1 else hou.append(i)
        return qian + hou
