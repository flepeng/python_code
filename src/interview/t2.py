# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/6  16:47
    @Author: Feng Lepeng
    @File  : t2.py
    @Desc  :
"""

ax = [1, 2]
ay = [3, 4]

bx = [2, 1]
by = [4, 3]

max_a_x = max([ax[0], ax[1]])
min_a_x = min([ax[0], ax[1]])
max_a_y = max([ay[0], ay[1]])
min_a_y = min([ay[0], ay[1]])

max_b_x = max([bx[0], bx[1]])
min_b_x = min([bx[0], bx[1]])
max_b_y = max([ay[0], by[1]])
min_b_y = min([by[0], by[1]])


if min_a_x > max_b_x or max_a_x < min_b_x:
    print(0)
else:
    if min_a_y > max_b_y or max_a_y < min_b_y:
        print(0)
    else:
        max_x = min([max_a_x, max_b_x])
        min_x = max([min_a_x, min_b_x])
        max_y = min([max_a_y, max_a_y])
        min_y = max([min_a_y, min_b_y])

        x = max_x - min_x
        y = max_y - min_y

        print(x*y)


if __name__ == '__main__':
    pass

