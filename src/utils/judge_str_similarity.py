# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2023/12/13 23:02
    @File   : judge_str_similarity.py
    @Desc   :
"""
import difflib
import Levenshtein


def string_similarity_1(str_1: str = None, str_2: str = None):
    return difflib.SequenceMatcher(None, str_1, str_2).quick_ratio()


def string_similarity_2(str1: str = None, str2: str = None):
    # https://blog.csdn.net/qq_44810930/article/details/135912689
    distance = Levenshtein.distance(str1, str2)
    similarity = 1 - (distance / max(len(str1), len(str2)))
    return similarity


if __name__ == '__main__':
    print(string_similarity_1("sdfajsldjflka", "sjaklfdjalfla"))
    print(string_similarity_2("sdfajsldjflka", "sjaklfdjalfla"))
