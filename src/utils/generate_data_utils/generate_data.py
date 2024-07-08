# -*- coding:utf-8 -*-
"""
    @Time  : 2023/11/2 16:27
    @Author: lepeng feng
    @File  : generate_data.py
    @Desc  : 随机生成 姓名、身份证、手机号
"""
import time
import random
import string
from ipaddress import IPv4Network
from generate_data_config import *

insert_data = []

name = boy_name + girl_name
first_name = boy_first + girl_first


class GenerateName(object):

    @classmethod
    def generate_surname(cls):
        """
        随机挑选姓
        :return:
        """
        return random.choice(surname)

    @classmethod
    def generate_name(cls):
        """
        随机生成名字
        :return:
        """
        ret_name = ""
        if random.random() > 0.5:
            ret_name = random.choice(name)
        else:
            for i in range(1, random.choice([2, 3])):
                ret_name += random.choice(first_name)

        return ret_name

    @classmethod
    def generate(cls):
        return cls.generate_surname() + cls.generate_name()


def get_random_char():
    # 汉字编码的范围是0x4e00 ~ 0x9fa5
    val = random.randint(0x4e00, 0x9fa5)
    # 转换为Unicode编码
    return chr(val)


class GeneratePhoneNumber(object):

    @classmethod
    def generate(cls):
        """
        生成一个随机的手机号
        :return:
        """
        area_code = ["13", "14", "15", "16", "17", "18", "19"]  # 手机号码前缀
        middle_number = str(random.randint(0, 99999)).zfill(5)  # 中间部分随机三位数，不足三位前面补零
        last_number = str(random.randint(0, 9999)).zfill(4)  # 最后四位随机数，不足四位前面补零

        phone_number = random.choice(area_code) + middle_number + last_number

        return phone_number


class GenerateId(object):
    @classmethod
    def generate(cls):
        """
        生成一个随机的身份证号码
        :return:
        """
        # 随机生成一个区域码(6位数)
        region_code = str(random.randint(110000, 659004))
        # 生成年份(4位数)
        year = str(random.randint(1949, 2023))
        # 生成月份(2位数)
        month = str(random.randint(1, 12)).rjust(2, '0')
        # 生成日期(2位数)
        day = str(random.randint(1, 28)).rjust(2, '0')
        # 生成顺序码(3位数)
        order = str(random.randint(1, 999)).rjust(3, '0')
        # 生成校验码(1位数)
        check_code = cls.get_check_code(region_code + year + month + day + order)
        # 拼接身份证号码并返回
        return 2023-int(year), "{}-{}-{}".format(year, month, day), region_code + year + month + day + order + check_code

    @classmethod
    def get_check_code(cls, id17):
        """
        计算校验码
        :param id17:
        :return:
        """
        # 系数列表
        factor_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        # 校验码列表
        check_code_list = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']
        # 根据前17位计算出校验码
        check_code = 0
        for i in range(len(id17)):
            check_code += int(id17[i]) * factor_list[i]
        check_code %= 11
        return check_code_list[check_code]


class GenerateEmail(object):
    @classmethod
    def generate(cls):
        domain = ["@163.com", "@qq.com", "@gmail.com", "@mail.hk.com", "＠yahoo.co.id", "mail.com", "gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
        username_length = random.randint(5, 10)

        username = ''.join(random.choices(string.ascii_lowercase, k=username_length))
        domain_name = random.choice(domain)
        email = username + "@" + domain_name

        return email


class GenerateCardId():

    @classmethod
    def generate(cls):
        card_id = '62'
        for i in range(17):
            tmp = str(random.randint(0,9))
            card_id += tmp
        return card_id


class GenerateIP():

    @classmethod
    def generate(cls, ip_type="IPv4"):
        if ip_type == "IPv4":
            address = ".".join(str(random.randint(0, 255)) for _ in range(4))
        elif ip_type == "IPv6":
            address = ":".join(hex(random.randint(1, 65535))[2:] for _ in range(8))
        else:
            address = None
        return address


if __name__ == "__main__":
    start_time = time.time()
    age, birthday, identity = GenerateId.generate()
    insert_data.append((GenerateName.generate(), "123456", age, random.choice([1, 2]), birthday,GeneratePhoneNumber.generate(), identity))
    print(insert_data)
    print(time.time()-start_time)
    print(GenerateCardId().generate())
    print(GenerateIP().generate())
