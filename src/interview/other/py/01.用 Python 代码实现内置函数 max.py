# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 17:52
    @File   : 01.用 Python 代码实现内置函数 max.py
    @Desc   :   这个题目看似简单，但实际上还是比较考察面试者的功底。因为 Python 内置的 `max` 函数既可以传入可迭代对象找出最大，又可以传入两个或多个参数找出最大；最为关键的是还可以通过命名关键字参数 `key` 来指定一个用于元素比较的函数，还可以通过`default`命名关键字参数来指定当可迭代对象为空时返回的默认值。
"""


def my_max(*args, key=None, default=None):
    """
    获取可迭代对象中最大的元素或两个及以上实参中最大的元素
    :param args: 一个可迭代对象或多个元素
    :param key: 提取用于元素比较的特征值的函数，默认为None
    :param default: 如果可迭代对象为空则返回该默认值，如果没有给默认值则引发ValueError异常
    :return: 返回可迭代对象或多个元素中的最大元素
    """
    if len(args) == 1 and len(args[0]) == 0:
        if default:
            return default
        else:
            raise ValueError('max() arg is an empty sequence')
    items = args[0] if len(args) == 1 else args
    max_elem, max_value = items[0], items[0]
    if key:
        max_value = key(max_value)
    for item in items:
        value = item
        if key:
            value = key(item)
        if value > max_value:
            max_elem, max_value = item, value
    return max_elem