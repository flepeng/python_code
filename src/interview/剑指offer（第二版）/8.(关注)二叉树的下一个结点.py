# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/2 20:46
    @File   : 8.(关注)二叉树的下一个结点.py
    @Desc   : 给定一个二叉树其中的一个结点，请找出中序遍历顺序的下一个结点并且返回。
              注意，树中的结点不仅包含左右子结点，同时包含指向父结点的next指针。
              牛客：https://www.nowcoder.com/practice/9023a0c988684a53960365b889ceaf5e?
"""


class TreeLinkNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.next = None


class Solution:
    def GetNext(self, pNode):
        """
        思路：如果该节点有右子树，则找右子树对应的最底层的左子树节点
              如果该节点没有右子树，则向上找父节点
                  如果该节点是父节点的左子树，则直接输出父节点
                  如果该节点是父节点的右子树，则继续向上查找
        :param pNode:
        :return:
        """
        if not pNode:
            return pNode
        # write code here
        if pNode.right:
            pNode = pNode.right
            while pNode.left:
                pNode = pNode.left
            return pNode
        while pNode.next:
            parent = pNode.next
            if parent.left == pNode:
                return parent
            pNode = parent
