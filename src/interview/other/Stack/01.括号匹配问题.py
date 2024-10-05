# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 16:53
    @File   : 01.括号匹配问题.py
    @Desc   :   给一个字符串，其中包含小括号、中括号、大括号，求该字符串中的括号是否匹配
"""


def brace_match(match_str):
    tmp_list = []
    d = {'(': ')', '[': ']', '{': '}'}
    for i in match_str:
        if i in d.keys():
            tmp_list.append(i)
        else:
            if not tmp_list:
                return False
            tmp = tmp_list.pop()
            if d[tmp] == i:
                continue
            else:
                return False
    if tmp_list:
        return False
    return True


if __name__ == '__main__':
    print(brace_match('[]{{}[]{()})}'))
    print(brace_match('[]{{}[]{()}}'))
