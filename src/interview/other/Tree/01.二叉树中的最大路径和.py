# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/6 18:19
    @File   : 01.二叉树中的最大路径和.py
    @Desc   :   https://leetcode.cn/problems/jC7MId/description/
                https://www.nowcoder.com/practice/8fda1d22554f4824b0ef9c26f35e54dd?tpId=230&tqId=39756&ru=/exam/oj
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxPathSum(self, root: TreeNode) -> int:
        ans = -inf

        def dfs(node) -> int:
            if node is None:
                return 0  # 没有节点，和为 0
            l_val = dfs(node.left)  # 左子树最大链和
            r_val = dfs(node.right)  # 右子树最大链和
            nonlocal ans
            ans = max(ans, l_val + r_val + node.val)  # 两条链拼成路径
            return max(max(l_val, r_val) + node.val, 0)  # 当前子树最大链和

        dfs(root)
        return ans
