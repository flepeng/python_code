# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/2 20:08
    @File  :
    @Desc  : 在一个长度为n的数组里的所有数字都在0到n-1的范围内。 数组中某些数字是重复的，但不知道有几个数字是重复的。也不知道每个数字重复几次。
             请找出数组中任意一个重复的数字。 例如，如果输入长度为7的数组{2,3,1,0,2,5,3}，那么对应的输出是第一个重复的数字2。
"""


class Solution:
    # 这里要特别注意：找到任意重复的一个值并赋值到 duplication[0]
    # 函数返回True/False
    def duplicate(self, numbers, ):
        for i, v in enumerate(numbers):
            if i != v:
                if numbers[v] == v:
                    return v
                numbers[i] = numbers[v]
                numbers[v] = v
                print(i, numbers)
        return False


if __name__ == '__main__':
    numbers = [2, 3, 4, 5, 6, 6, 4, 2]
    print(Solution().duplicate(numbers))
