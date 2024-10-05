# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 16:45
    @File   : 03.按照单词反转给定句子.py
    @Desc   : 例如，输入"what is your name"，返回 "name your is what"。请不要使用诸如`''.split`, `[::-1]` 等时间/空间复杂度不是O(1)的函数
"""


def str_reverse(old_str):
    tmp = ""
    new_str = ""
    for i in old_str:
        if i == " ":
            new_str = tmp + " " + new_str
            tmp = ""
        else:
            tmp += i

    new_str = tmp + " " + new_str
    return new_str


def str_reverse_1(str, i, j):
    while i < j:
        str[i], str[j] = str[j], str[i]
        i += 1
        j -= 1


def sentence_reverse(sentence):
    sent_list = list(sentence)
    i = 0
    len_list = len(sent_list)
    while i < len_list:
        if sent_list[i] != ' ':
            start = i
            end = start + 1
            while (end < len_list) and (sent_list[end] != ' '):
                end += 1
            str_reverse_1(sent_list, start, end - 1)
            i = end
        else:
            i += 1
    sent_list.reverse()
    return (''.join(sent_list))


if __name__ == '__main__':
    print(str_reverse("what is your name"))
