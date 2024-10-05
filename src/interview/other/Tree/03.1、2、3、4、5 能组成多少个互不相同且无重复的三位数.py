# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/3 22:51
    @File   : 03.1、2、3、4、5 能组成多少个互不相同且无重复的三位数.py
    @Desc   :
                题意理解：组成后的数值不相同，且组合的三个位数之间数字不重复。

                使用 Python 内置的排列组合函数（不放回抽样排列）

                *   `product` 笛卡尔积  （有放回抽样排列）
                *   `permutations` 排列  （不放回抽样排列）
                *   `combinations` 组合，没有重复  （不放回抽样组合）
                *   `combinations_with_replacement` 组合，有重复  （有放回抽样组合）
"""

import itertools

print(len(list(itertools.permutations('12345', 3))))  # 60个
