# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/15 11:41
    @File   : 9.一个队列实现栈.py
    @Desc   :   *   `Stack()` 创建一个新的空栈
                *   `push(item)` 添加一个新的元素item到栈顶
                *   `pop()` 弹出栈顶元素
                *   `peek()` 返回栈顶元素
                *   `is_empty()` 判断栈是否为空
                *   `size()` 返回栈的元素个数
"""


# 实现一个栈stack,后进先出
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        # 判断是否为空
        return self.items == []

    def push(self, item):
        # 加入元素
        self.items.append(item)

    def pop(self):
        # 弹出元素
        return self.items.pop()

    def peek(self):
        # 返回栈顶元素
        return self.items[len(self.items) - 1]

    def size(self):
        # 返回栈的大小
        return len(self.items)


if __name__ == "__main__":
    stack = Stack()
    stack.push("H")
    stack.push("E")
    stack.push("L")
    print(stack.size())  # 3
    print(stack.peek())  # L
    print(stack.pop())  # L
    print(stack.pop())  # E
    print(stack.pop())  # H
