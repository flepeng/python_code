# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/9 23:00
    @File   : 31.(常考)栈的压入弹出序列.py
    @Desc   : 输入两个整数序列，第一个序列表示栈的压入顺序，请判断第二个序列是否可能为该栈的弹出顺序。
              假设压入栈的所有数字均不相等。
              例如序列1,2,3,4,5是某栈的压入顺序，序列4,5,3,2,1是该压栈序列对应的一个弹出序列，但4,3,5,1,2就不可能是该压栈序列的弹出序列。
              注意：若两个序列长度不等则视为并不是一个栈的压入、弹出序列。若两个序列都为空，则视为是一个栈的压入、弹出序列。
              https://leetcode.cn/problems/validate-stack-sequences/submissions/545553064/
"""


class Solution:
    def validateStackSequences(self, pushed: list[int], popped: list[int]) -> bool:
        tmp = popped.pop(0)
        tmp_list = []

        for i in pushed:
            if i == tmp:
                if not popped:
                    return True
                tmp = popped.pop(0)
                while popped and tmp_list and tmp == tmp_list[-1]:
                    tmp = popped.pop(0)
                    tmp_list.pop()

            else:
                tmp_list.append(i)
        if popped:
            return False
        return True

