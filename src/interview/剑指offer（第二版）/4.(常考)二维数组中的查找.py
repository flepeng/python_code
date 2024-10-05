# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/2 20:08
    @File  :
    @Desc  : 在一个二维数组中（每个一维数组的长度相同），每一行都按照从左到右递增的顺序排序，每一列都按照从上到下递增的顺序排序。
             请完成一个函数，输入这样的一个二维数组和一个整数，判断数组中是否含有该整数。
"""


class Solution:
    def find(self, target, array):
        row_len = len(array[0])
        line_len = len(array)
        i = 0
        j = line_len - 1

        while i < row_len and j >= 0:
            if array[j][i] == target:
                return i, j
            elif array[j][i] > target:
                j -= 1
            elif array[j][i] < target:
                i += 1
        else:
            return False



if __name__ == '__main__':
    pass