# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 10:50
    @File   : 12.矩阵中的路径.py
    @Desc   :  https://leetcode.cn/problems/word-search/
"""


class Solution:

    def exist(self, board: list[list[str]], word: str) -> bool:
        self.hava_flag = False
        row_len = len(board)
        world_len = len(board[0])

        def judge(i, j, h):
            if h >= len(word):
                self.hava_flag = True
                return
            original, board[i][j] = board[i][j], '-'
            for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                if 0 <= x < row_len and 0 <= y < world_len:
                    if board[x][y] == word[h]:
                        judge(x, y, h + 1)
            board[i][j] = original

        for i in range(0, row_len):
            for j in range(0, world_len):
                if board[i][j] == word[0]:
                    judge(i, j, 1)

        return self.hava_flag


