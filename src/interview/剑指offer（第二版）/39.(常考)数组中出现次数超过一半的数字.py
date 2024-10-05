# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/11 17:35
    @File   : 39.(常考)数组中出现次数超过一半的数字.py
    @Desc   :   https://leetcode.cn/problems/majority-element
"""


# 方法一：排序. Time-O(nlogn), Space-O(n)
def majority_element(nums):
    return sorted(nums)[len(nums) // 2]


# 方法二：Counter Time-O(n), Space-O(n)
def majority_element(nums):
    from collections import Counter
    c = Counter(nums)
    # return max(c.keys(), key=c.get)
    return c.most_common(1)[0][0]


# 方法三：Boyer-Moore Voting Algorithm. 书中的算法说的就是这个，这详情请看[波义尔摩尔投票](https://darktiantian.github.io/%E6%B3%A2%E4%B9%89%E5%B0%94%E6%91%A9%E5%B0%94%E6%8A%95%E7%A5%A8%E7%AE%97%E6%B3%95%EF%BC%88Boyer-Moore-Voting-Algorithm%EF%BC%89/)。
def majorityElement(self, nums):
    count = 0
    candidate = None
    for num in nums:
        if count == 0:
            candidate = num
        count += (1 if num == candidate else -1)
    return candidate
