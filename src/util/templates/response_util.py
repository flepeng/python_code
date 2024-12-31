# -*- coding:utf-8 -*-
"""
    @Time  : 2023/9/18
    @Author: Feng Lepeng
    @File  :
    @Desc  :
"""
import json


class Response:

    @staticmethod
    def success(data={}, message="success"):
        response = {
            "code": 200,
            "message": message,
            "data": data,
        }
        return json.dumps(response, ensure_ascii=False)

    @staticmethod
    def failure(code="500", message="fail"):
        response = {
            "code": code,
            "message": message,
            "data": "",
        }
        return json.dumps(response, ensure_ascii=False)

    def custom(self):
        pass
