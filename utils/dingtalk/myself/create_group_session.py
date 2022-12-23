# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/24  17:05
    @Author: Feng Lepeng
    @File  : create_group_session.py
    @Desc  : 创建群会话 https://open.dingtalk.com/document/orgapp-server/create-group-session
"""
import json
import requests

url = "https://oapi.dingtalk.com/chat/create?access_token=f5368a8230073d7f8adeb80aabbbc6cd"

data = {
    "name": "SEM 测试群",
    "owner": "163560584720757486",
    "useridlist": ["062541521921189223", ],
    # "useridlist": ["062541521921189223", "225315361139140174"],
    "showHistoryType": 1,
    "searchable": 0,
    "validationType": 0,
    "mentionAllAuthority": 0,
    "managementType": 0,
    "chatBannedType": 0
}

try:
    resp = requests.post(url, data=json.dumps(data))
    print(resp)
    print(resp.text)
except Exception as e:
    print(e)
