# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/3 20:35
    @File   : 9.(关注)用两个栈实现队列.py
    @Desc   : 用两个栈来实现一个队列，完成队列的Push和Pop操作。 队列中的元素为int类型。
"""


class MyQueue():
    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def push(self, data):
        self.stack1.append(data)

    def pop(self):
        if not self.stack2:
            if not self.stack1:
                return None
            else:
                while self.stack1:
                    tmp = self.stack1.pop()
                    self.stack2.append(tmp)

        return self.stack2.pop()
