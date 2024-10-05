# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 11:08
    @File   : 13.(关注)机器人的运动范围.py
    @Desc   : https://www.nowcoder.com/practice/6e5207314b5241fb83f2329e89fdecc8?
"""


class Solution:
    def movingCount(self, threshold: int, rows: int, cols: int) -> int:
        visited = [[False] * cols for _ in range(rows)]

        def get_sum(x, y):
            res = 0
            while x:
                res += x % 10
                x = x // 10
            while y:
                res += y % 10
                y = y // 10
            return res

        def movingCore(threshold, rows, cols, i, j):
            if get_sum(i, j) <= threshold:
                visited[i][j] = True
                for x, y in ((i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)):
                    if 0 <= x < rows and 0 <= y < cols and not visited[x][y]:
                        movingCore(threshold, rows, cols, x, y)

        movingCore(threshold, rows, cols, 0, 0)
        return sum(sum(visited, []))
