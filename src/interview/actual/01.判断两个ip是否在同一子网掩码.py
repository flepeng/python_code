# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/7/4 23:13
    @File   : 01.判断两个ip是否在同一子网掩码.py
    @Desc   :
"""


def calculate_network_address(ip, mask):
    ip_list = ip.split(".")
    mask_list = mask.split(".")
    new = []
    for i in range(4):
        new.append(ip_list[i] & mask_list[i])  # python 可以直接 与，不需要转换成 二 进制。
    return ".".join(new)


def calculate_mask(num):
    if 0 < num <= 8:
        return "{}.0.0.0".format((2 ** num - 1) << (8 - num))
    if 8 < num <= 16:
        return "255.{}.0.0".format((2 ** (num - 8) - 1) << (16 - num))
    if 16 < num <= 24:
        return "255.255.{}.0".format((2 ** (num - 16) - 1) << (24 - num))
    if 24 < num <= 32:
        return "255.255.255.{}".format((2 ** (num -24) - 1) << (32 - num))


if __name__ == '__main__':
    ret = calculate_mask(31)
    print(ret)
