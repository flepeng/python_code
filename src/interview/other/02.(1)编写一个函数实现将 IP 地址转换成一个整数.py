# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/9/2 16:19
    @File   : 02.编写一个函数实现将 IP 地址转换成一个整数.py
    @Desc   :
                如 10.3.9.12 转换规则为：
                    10           00001010
                    3            00000011 
                    9            00001001
                    12           00001100 
                再将以上二进制拼接起来计算十进制结果：00001010 00000011 00001001 00001100 = ?
"""
# 第一种
ip_addr = '192.168.2.10'


# transfer ip to int
def ip2long_1(ip):
    ip_list = ip.split('.')
    result = 0
    for i in range(4):  # 0,1,2,3
        result = result + int(ip_list[i]) * 256 ** (3 - i)
    return result


# transfer int to ip
def long2ip_1(long):
    floor_list = []
    yushu = long
    for i in reversed(range(4)):  # 3,2,1,0
        res = divmod(yushu, 256 ** i)
        floor_list.append(str(res[0]))
        yushu = res[1]
    return '.'.join(floor_list)


# 第二种
def ip2long_2(addr):
    addr_list = addr.split(".")
    return sum([int(addr_list[i]) << [24, 16, 8, 0][i] for i in range(4)])


if __name__ == '__main__':
    print(ip2long_1("127.0.0.1"))
    print(ip2long_2("127.0.0.1"))
    print(long2ip_1(3232236042))
