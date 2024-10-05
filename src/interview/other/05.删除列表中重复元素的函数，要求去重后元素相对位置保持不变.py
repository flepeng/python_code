# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 17:37
    @File   : 05.删除列表中重复元素的函数，要求去重后元素相对位置保持不变.py
    @Desc   :   这个题目在初中级 Python 岗位面试的时候经常出现，题目源于《Python Cookbook》这本书第一章的第10个问题，有很多面试题其实都是这本书上的原题，所以建议大家有时间好好研读一下这本书。
"""

# Python 中的集合底层使用哈希存储，所以集合的 `in` 和 `not in` 成员运算在性能上远远优于列表，所以上面的代码我们使用了集合来保存已经出现过的元素
# 集合中的元素必须是 `hashable` 对象，因此上面的代码在列表元素不是 `hashable` 对象时会失效，要解决这个问题可以给函数增加一个参数，该参数可以设计为返回哈希码或 `hashable` 对象的函数
def dedup(items):
    no_dup_items = []
    seen = set()
    for item in items:
        if item not in seen:
            no_dup_items.append(item)
            seen.add(item)
    return no_dup_items
