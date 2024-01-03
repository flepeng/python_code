# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/21  17:13
    @Author: Feng Lepeng
    @File  : t8.py
    @Desc  :
"""


class Node():
    def __init__(self, val):
        self.val = val
        self.next = None


n1 = Node(9)
n2 = Node(9)
n3 = Node(9)
n4 = Node(9)
n1.next = n2
n2.next = n3
n3.next = n4

n11 = Node(1)
n21 = Node(0)
n31 = Node(1)
# n41 = Node(4)
# n51 = Node(5)
n11.next = n21
n21.next = n31
# n31.next = n41
# n41.next = n51

l1 = n1
l2 = n11

l3 = Node(0)

tmp_l1 = l1
tmp_l2 = l2
tmp_l3 = l3
tmp = 0

while tmp_l1 and tmp_l2:
    count = tmp_l1.val + tmp_l2.val + tmp
    if count >= 10:
        g = count % 10
        tmp = 1
    else:
        g = count
        tmp = 0
    tmp_node = Node(g)
    tmp_l3.next = tmp_node
    tmp_l3 = tmp_l3.next
    tmp_l1 = tmp_l1.next
    tmp_l2 = tmp_l2.next

while tmp_l1:
    count = tmp_l1.val + tmp
    if count >= 10:
        g = count % 10
        tmp = 1
    else:
        g = count
        tmp = 0
    tmp_l3.next = Node(g)
    tmp_l3 = tmp_l3.next
    tmp_l1 = tmp_l1.next

while tmp_l2:
    count = tmp_l2.val + tmp
    if count >= 10:
        g = count % 10
        tmp = 1
    else:
        g = count
        tmp = 0
    tmp_l3.next = Node(g)
    tmp_l3 = tmp_l3.next
    tmp_l2 = tmp_l2.next

if tmp == 1:
    tmp_l3.next = Node(1)

tmp = l3.next

while tmp:
    print(tmp.val)
    tmp = tmp.next


if __name__ == '__main__':
    pass
