# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/20  18:23
    @Author: Feng Lepeng
    @File  : t7.py
    @Desc  :
"""

def wrapper1(f1):
    print('in wrapper1')
    def inner1(*args,**kwargs):
        print('in inner1')
        ret = f1(*args,**kwargs)
        print('111')
        return ret
    return inner1

def wrapper2(f2):
    print('in wrapper2')
    def inner2(*args,**kwargs):
        print('in inner2')
        ret = f2(*args,**kwargs)
        print('222')
        return ret
    return inner2

def wrapper3(f3):
    print('in wrapper3')
    def inner3(*args,**kwargs):
        print('in inner3')
        ret = f3(*args,**kwargs)
        print('333')
        return ret
    return inner3

@wrapper1  #3 func = wrapper1(func)即 func = wrapper2(inner2) -->f1 = inner2 -->打印in wrapper1 --> func = inner1
@wrapper2  #2 func = wrapper2(func)即 func = wrapper2(inner3) -->f2 = inner3 --> 打印in wrapper2 --> func = inner2
@wrapper3  #1 func = wrapper3(func) --> f3 = func -->打印in wrapper3 --> func = inner3
def func(): # 先执行离被装饰函数最近的那个装饰器
    print('in func')
func() #4 func = inner1


if __name__ == '__main__':
    pass

