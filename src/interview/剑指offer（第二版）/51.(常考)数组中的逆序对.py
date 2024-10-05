# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/12 19:04
    @File   : 51.(常考)数组中的逆序对.py
    @Desc   :   https://www.nowcoder.com/practice/96bd6684e04a44eb80e6a68efc0ec6c5
"""


#
# 代码中的类名、方法名、参数名已经指定，请勿修改，直接返回方法规定的值即可
#
#
# @param data int整型一维数组
# @return int整型
#
class Solution:
    def __init__(self):
        self.num = 0

    def InversePairs(self, data: list[int]) -> int:
        # write code here
        def merge_sort(data):
            # print(data)
            count = len(data)
            if count > 1:
                mid = count // 2
                left = merge_sort(data[: mid])
                right = merge_sort(data[mid:])
                return merge(left, right)
            else:
                return data

        def merge(left, right):
            ret = []

            l_left = len(left)
            l_right = len(right)

            l = 0
            r = 0

            while l < l_left and r < l_right:
                if left[l] <= right[r]:
                    ret.append(left[l])
                    l += 1
                else:
                    ret.append(right[r])
                    self.num += l_left - l
                    r += 1

            if l < l_left:
                ret.extend(left[l:])

            if r < l_right:
                ret.extend(right[r:])
            print(ret)
            return ret

        merge_sort(data)
        print(self.num)
        return self.num % 1000000007