# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/5  20:50
    @Author: Feng Lepeng
    @File  : t1.py
    @Desc  :
"""

import random

GroupList = [  # 小组列表
    ['小名', '小红', '小马', '小丽', '小强'],
    ['大壮', '大力', '大1', '大2', '大3'],
    ['阿花', '阿朵', '阿蓝', '阿紫', '阿红'],
    ['A', 'B', 'C', 'D', 'E'],
    ['一', '二', '三', '四', '五'],
    ['建国', '建军', '建民', '建超', '建跃'],
    ['爱民', '爱军', '爱国', '爱辉', '爱月']
]


def find_max(li):
    ret = 0
    for i in range(len(li)):
        if li[ret] < li[i]:
            ret = i
    return ret


result = []
count = 0
count_1 = len(GroupList)
count_1_list = []
for i in range(count_1):
    tmp_len = len(GroupList[i])
    count_1_list.append(tmp_len)
    count += tmp_len

for i in range(count // 2):
    j = find_max(count_1_list)
    tmp_1 = GroupList[j][0]
    GroupList[j].remove(tmp_1)
    count_1_list[j] -= 1

    tmp_2 = None
    tmp_list = [i for i in range(count_1) if i != j]

    while not tmp_2:
        tmp_hang = random.choice(tmp_list)
        if len(GroupList[tmp_hang]) > 0:
            tmp_2 = random.choice(GroupList[tmp_hang])
            GroupList[tmp_hang].remove(tmp_2)
            count_1_list[tmp_hang] -= 1
    result.append([tmp_1, tmp_2])

for i in range(count_1):
    if len(GroupList[i]) >= 1:
        tmp = random.randint(0, len(result))
        result[tmp].append(GroupList[i][0])

print(result)

if __name__ == '__main__':
    pass
