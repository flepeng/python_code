# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/1  14:05
    @Author: Feng Lepeng
    @File  : t.py
    @Desc  :
"""

import time


def warp_1(func):
    d = {"num": 0, "count": 0}  # 注意这个地方是字典，因为字典的话，传的是引用。如果是str 的话，传的是值。

    def f(*args, **kwargs):
        d["num"] = d["num"] + 1
        start_time = time.time()
        ret = func(*args, **kwargs)
        d["count"] = d["count"] + time.time() - start_time
        if d["num"] % 10 == 0:
            print(d["num"], d["count"] / d["num"])
        return ret

    return f


def warp(num):
    d = {"num": 0, "count": 0}

    def f1(func):
        def f(*args, **kwargs):
            d["num"] = d["num"] + 1
            start_time = time.time()
            ret = func(*args, **kwargs)
            d["count"] = d["count"] + time.time() - start_time
            if d["num"] % num == 0:
                print(d["num"], d["count"] / d["num"])
            return ret

        return f

    return f1


@warp(10)
def t():
    time.sleep(0.1)


for i in range(12):
    t()


class Tree():
    def __init__(self, num):
        self.num = num
        self.left = None
        self.right = None


t1 = Tree(1)


def deep(t: Tree):
    tmp_list = []
    if t is None:
        return 0
    count = 0
    tmp_list.append(t)

    while len(tmp_list) != 0:
        num = len(tmp_list)
        count += 1
        for i in range(num):
            tmp_t = tmp_list.pop()
            if tmp_t.left:
                tmp_list.append(tmp_t.left)
            if tmp_t.right:
                tmp_list.append(tmp_t.right)

    return count


d = {}

d["key"] = "345"
d["name"] = "124"

for k, v in d.items():
    print(k, v)

li = [[1], [2, [3]]]


def get_max(li):
    print(li)
    tmp_max = 0
    if not isinstance(li, list):
        return tmp_max
    for i in li:
        tmp = get_max(i)
        tmp_max = max([tmp_max, tmp])
    return tmp_max + 1

print(get_max(li))

if __name__ == '__main__':
    pass
