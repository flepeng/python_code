# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/3 17:59
    @File   : 01.python_sort.py
    @Desc   :
"""

"""
list.sort(key=None, reverse=False)

参数：
    key：主要是用来指定进行比较的元素，只有一个参数，具体的函数的参数就是取自于可迭代对象中，指定可迭代对象中的一个元素来进行排序。
    reverse：排序规则，reverse = True 降序， reverse = False 升序（默认）。
"""
l = [1, 5, 6, 3, 2]
l.sort(reverse=True)  # 降序
print(l)  # [1, 2, 3, 5, 6]

"""
# Python2 中
sorted(iterable, cmp=None, key=None, reverse=False)

# Python3 中。Python3 相比于 Python2 废弃了 `cmp` 参数
sorted(iterable，key=None,reverse=False)
"""

print(sorted([5, 2, 3, 1, 4]))  # [1, 2, 3, 4, 5]
# 降序排序
print(sorted([5, 2, 3, 1, 4], reverse=True))  # [5, 4, 3, 2, 1]

"""
Python3 废弃了 Python2 中 sorted 函数的 `cmp` 参数。 所以我们只能使用 `key` 参数进行排序，
如果非要使用cmp函数进行自定义排序的话，可以**借助 `functools` 模块中的 `cmp_to_key` 函数**。
"""


def comp(x, y):
    if x < y:
        return 1
    elif x > y:
        return -1
    else:
        return 0


from functools import cmp_to_key

d = {"a": 4, "c": 3, "b": 2, "d": 2}
dic = sorted(d.items(), key=cmp_to_key(comp))
print(dic)  # [('d', 2), ('c', 3), ('b', 2), ('a', 4)]
