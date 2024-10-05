# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/11 16:13
    @File   : ttt.py
    @Desc   :
"""


def my_permutation(s):
    str_set = []
    ret = []  # 最后的结果

    def permutation(string):
        for i in string:
            str_tem = string.replace(i, '')
            str_set.append(i)
            if len(str_tem) > 0:
                permutation(str_tem)
            else:
                ret.append(''.join(str_set))
            str_set.pop()

    permutation(s)
    return ret


class Solution:
    def permutation(self, nums):
        perms = [[]]
        for n in nums:
            tmp = []
            # perms = [
            #     p[:i] + [n] + p[i:]
            #     for p in perms
            #     for i in range((p+[n]).index(n)+1)]
            for p in perms:
                for i in range((p+[n]).index(n)+1):
                    tmp.append(p[:i] + [n] + p[i:])
            perms = tmp
        return perms


def t(*args, **kwargs):
    print(args)
    print(kwargs)


if __name__ == '__main__':
    # my_permutation("abcdefg")
    # ret = Solution().permutation("abcdeft")
    # print(ret)
    t()