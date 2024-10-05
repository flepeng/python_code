# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/5 17:12
    @File   : 01.二叉树种的最大路劲和（从根节点出发）.py
    @Desc   :
"""


class Tree():
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


t1 = Tree(1)
t2 = Tree(3)
t3 = Tree(4)
t4 = Tree(5)
t5 = Tree(6)
t6 = Tree(7)
t7 = Tree(8)

t1.left = t2
t1.right = t3
t2.left = t4
t2.right = t5
t3.left = t6
t3.right = t7


def func(tree):
    tmp_tree = tree
    tmp_list = [tree]
    while True:
        if tmp_tree.left and tmp_tree.rirht:
            if tmp_tree.left > tmp_tree.right:
                tmp_tree = tree.left
                tmp_list.append(tmp_tree)
            else:
                tmp_tree = tree.right
                tmp_list.append(tmp_tree)
        elif tmp_tree.left:
            tmp_tree = tree.left
            tmp_list.append(tmp_tree)
        elif tmp_tree.right:
            tmp_tree = tree.right
            tmp_list.append(tmp_tree)
        else:
            break


def func_2(tree):
    if tree.left:
        left_count, left_list = func_2(tree.left)
    if tree.right:
        right_count, right_list = func_2(tree.right)
    if tree.left and tree.right:
        if left_count > right_count:
            return left_count + tree.val, left_list + [tree]
        else:
            return right_count + tree.val, right_list + [tree]
    elif tree.left:
        return left_count + tree.val, left_list + [tree]
    elif tree.right:
        return right_count + tree.val, right_list + [tree]
    else:
        return tree.val, [tree]


if __name__ == '__main__':
    num, tmp_list = func_2(t1)
    print(num)
    print([i.val for i in tmp_list])
