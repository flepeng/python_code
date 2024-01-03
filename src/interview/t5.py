# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/12  10:39
    @Author: Feng Lepeng
    @File  : t5.py
    @Desc  :
"""
import ctypes
import string

arr_1067 = [
    0xf1, 0xa7, 0xf0, 0x07, 0xed,
]


def encode(char, index):
    assert (len(arr_1067) == 5)
    var_j = 4 - (index % len(arr_1067))
    var_l = arr_1067[var_j]
    var_n = ctypes.c_int32(var_l << 24).value
    var_o = ctypes.c_int32(var_n >> 24).value
    var_q = ctypes.c_int32(ord(char) ^ var_o).value
    res = ctypes.c_uint8(var_q).value
    return res


arr_1024 = [
    0x9d, 0x6e, 0x93, 0xc8, 0xb2, 0xb9, 0x41, 0x8b, 0xc2, 0x97, 0xd4, 0x66, 0xc7, 0x93, 0xc4, 0xd4, 0x61, 0xc2, 0xc6, 0xc9, 0xdd, 0x62,
    0x94, 0x9e, 0xc2, 0x89, 0x32, 0x91, 0x90, 0xc1, 0xdd, 0x33, 0x91, 0x91, 0x97, 0x8b, 0x64, 0xc1, 0x92, 0xc4, 0x90, 0x00, 0x00
]

for i in range(len(arr_1024)):
    for c in string.printable:
        if encode(c, i) == arr_1024[i]:
            print(c, end="")

print("")

if __name__ == '__main__':
    pass
