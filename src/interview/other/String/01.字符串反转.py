# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 17:56
    @File   : 01.字符串反转.py
    @Desc   :   这些方法其实都是大同小异的，面试的时候能够给出几种有代表性的就足够了。
"""


# 方法一：反向切片
def reverse_string_1(content):
    return content[::-1]


# 方法二：反转拼接
def reverse_string_2(content):
    return ''.join(reversed(content))


# 方法三：递归调用
def reverse_string_3(content):
    if len(content) <= 1:
        return content
    return reverse_string(content[1:]) + content[0]


# 方法四：双端队列
from collections import deque


def reverse_string_4(content):
    q = deque()
    q.extendleft(content)
    return ''.join(q)


# 方法五：反向组装
from io import StringIO


def reverse_string_5(content):
    buffer = StringIO()
    for i in range(len(content) - 1, -1, -1):
        buffer.write(content[i])
    return buffer.getvalue()


# 方法六：反转拼接
def reverse_string_6(content):
    return ''.join([content[i] for i in range(len(content) - 1, -1, -1)])


# 方法七：半截交换
def reverse_string_7(content):
    length, content = len(content), list(content)
    for i in range(length // 2):
        content[i], content[length - 1 - i] = content[length - 1 - i], content[i]
    return ''.join(content)


# 方法八：对位交换
def reverse_string_8(content):
    length, content = len(content), list(content)
    for i, j in zip(range(length // 2), range(length - 1, length // 2 - 1, -1)):
        content[i], content[j] = content[j], content[i]
    return ''.join(content)
