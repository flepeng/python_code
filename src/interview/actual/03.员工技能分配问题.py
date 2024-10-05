# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/8/13 11:55
    @File   : 03.员工技能分配问题.py
    @Desc   :
"""

"""
背景：
一家公司拥有 M 名员工（M 是一个正整数），每位员工有各自的技能等级（一个正整数），表示为一个整数数组 skills，但技能越高费用越高。公司计划启动 N 个项目（N <= M），每个项目需要指定一名负责人，且每个项目的难度等级（一个正整数）已知，表示为一个整数数组 project_difficulties。
规则：
	•	每位员工只能负责一个项目，每个项目只能有一名负责人。
	•	员工负责项目的难度不能超过其自身的技能等级。
	•	公司的目标是总技能等级之和最优。
任务：
编写一个程序，输入员工技能数组 skills 和项目难度数组 project_difficulties，输出一个有效的项目负责人分配方案，使得公司在这些项目上的投入费用最低。
示例：
输入：
skills = [3, 5, 7, 6] tmp_i
project_difficulties = [2, 4, 6]
输出：
分配方案为：员工 1 负责项目 1，员工 2 负责项目 2，员工 4 负责项目 3，总技能等级之和为 14。
"""


def func(skills, project_difficulties):
    skills.sort()
    project_difficulties.sort()
    print(skills, project_difficulties)
    tmp = []
    tmp_i = 0
    for project_difficultie in project_difficulties:
        while skills[tmp_i] < project_difficultie and tmp_i < len(skills):
            tmp_i += 1
        if tmp_i < len(skills):
            tmp.append(skills[tmp_i])
        tmp_i += 1
        if tmp_i >= len(skills) and len(tmp) != len(project_difficulties):
            print("error")
            break
    print("=====", tmp)
    return tmp


if __name__ == '__main__':
    skills = [3, 5, 7, 6]
    project_difficulties = [2, 4, 6]

    # skills = [3, 5, 7, 6]
    # project_difficulties = [2, 6, 6, 5]

    # skills = [3, 5, 7, 6, 8]
    # project_difficulties = [2, 6, 6, 6]

    ret = func(skills, project_difficulties)
    # print(ret)
    # print(sum(ret))
