# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/9 22:54
    @File   : 26.(常考)树的子结构.py
    @Desc   : 要求：判断一棵二叉树是不是另一个的子结构
              https://leetcode.cn/problems/subtree-of-another-tree/
"""


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def isPart(self, p1, p2):

        if not p2:
            return True
        if not p1 or p1.val != p2.val:
            return False
        return self.isPart(p1.left, p2.left) and self.isPart(p1.right, p2.right)

    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        if not subRoot:
            return False

        if self.isPart(root, subRoot):
            return True

        if not root or not subRoot:
            return False

        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
