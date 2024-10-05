# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/3 21:03
    @File   : 11.(常考)旋转数组中的最小数字.py
    @Desc   : 把一个数组最开始的若干个元素搬到数组的末尾，我们称之为数组的旋转。
                输入一个非递减排序的数组的一个旋转，输出旋转数组的最小元素。
                例如数组{3,4,5,1,2}为{1,2,3,4,5}的一个旋转，该数组的最小值为1。
                NOTE：给出的所有元素都大于0，若数组大小为0，请返回0。
                https://leetcode.cn/problems/find-minimum-in-rotated-sorted-array/
"""


class Solution:
    def findMin(self, nums: list[int]) -> int:

        if nums[0] < nums[-1]:
            return nums[0]
        left = 0

        right = len(nums) - 1

        if right == 0:
            return nums[0]

        while left < right:
            mid = (left + right) // 2
            if nums[mid] > nums[left]:
                left = mid
            elif nums[mid] < nums[left]:
                right = mid
            else:
                return nums[right]
