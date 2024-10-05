# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/2 20:12
    @File   : 7.(关注)重建二叉树.py
    @Desc   : 输入某二叉树的前序遍历和中序遍历的结果，请重建出该二叉树。
              假设输入的前序遍历和中序遍历的结果中都不含重复的数字。例如输入前序遍历序列{1,2,4,7,3,5,6,8}和中序遍历序列{4,7,2,1,5,3,8,6}，则重建二叉树并返回。
                1
              2  3
            4   5 6
             7   8

"""


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def rebuild_tree(self, preorder, inorder):
        if not preorder or not inorder:
            return
        TreeNode.val = preorder[0]
        index = inorder.index(inorder[0])
        TreeNode.left = self.rebuild_tree(preorder[1:], inorder[0:index - 1])
        TreeNode.right = self.rebuild_tree(preorder[index+1:], inorder[index + 1:])
        return TreeNode