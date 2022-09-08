# -*- coding:utf-8 -*-
"""
    @Time  : 2022/1/26  11:24
    @Author: Feng Lepeng
    @File  : .py
    @Desc  :
"""
import os
import json
import time
import hmac
import base64
import urllib
import hashlib
import requests
from utils.op_ini import conf


class ResponseParse(object):

    def __init__(self, data):
        self.err_code = data.get("errcode")
        self.err_msg = data.get("errmsg")
        self.request_id = data.get("request_id")
        self.result = data.get("result")
        if self.err_code:
            print(data)
            raise KeyError("发生错误")


class DingTalk(object):

    def __init__(
            self,
            app_id: str = conf.DINGTALK_AGENT_ID,
            app_key: str = conf.DINGTALK_APP_KEY,
            app_secret: str = conf.DINGTALK_APP_SECRET
    ):
        self.app_id = app_id
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = ""
        self.get_access_token()

        self.webhook = ""
        self.sign = ""
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.user_list = []
        self.dept_id_list = [
            469890217, 469854248, 470304064, 470173083, 469916201, 475662415, 484646128, 503123846,
            470260061, 470186089, 469989194, 469978130, 550047304, 469052993, 469905208, 396701474,
            305875441, 366794646, 493997019, 322021373, 399721727, 486117544, 391394241, 558894502,
            407234930, 387342285, 414715620, 410907971, 561135276, 503569125, 503584098, 503595085,
            577417710, 577199749, 426311497, 469914246, 450491420, 469952165, 469793322, 558544934,
            73695179, 470389030, 418248345, 574303727, 418515689, 470124089, 592871370, 124550033,
            399544333, 543592379, 469933181, 577027867, '1']

    def get_access_token(self):
        """
        获取 access token
        :return:
        """
        url = "https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}".format(self.app_key, self.app_secret)
        resp = requests.get(url)
        if resp.json().get("errcode") == 0:
            self.access_token = resp.json().get("access_token")
            return
        raise KeyError("发生错误")

    def create_sign(self):
        """
        加密签名，必须，官方提供
        """
        timestamp = int(round(time.time() * 1000))
        secret = self.sign
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(
            secret_enc,
            string_to_sign_enc,
            digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    def splice_url(self):
        """
        拼接 url
        :return:
        """
        timestamp, sign = self.create_sign()
        url = '{}&timestamp={}&sign={}'.format(self.webhook, timestamp, sign)
        return url

    def send_text(self, msg, msgtype="text"):
        """
        发送 text 类型的消息
        :param msg:
        :return:
        """
        if not msg:
            return {'errcode': 500, 'errmsg': '消息内容不能为空'}

        data = {
            "msgtype": msgtype,
            "at": {},
            "text": {"content": msg}
        }

        post_data = json.dumps(data)
        try:
            response = requests.post(
                self.splice_url(),
                headers=self.headers,
                data=post_data
            )
        except Exception:
            return {'errcode': 500, 'errmsg': '服务器响应异常'}

        result = response.json()
        return result

    def get_user_list(self, dept_id: str = "1", next_cursor: int = 0):
        """
        获取部门员工信息, 每次获取 100 个
        :param dept_id: 部门id
        :param next_cursor: 获取的游标开始地址
        :return:
        """
        url = "https://oapi.dingtalk.com/topapi/v2/user/list?access_token={}".format(self.access_token)
        data = {
            "cursor": next_cursor,
            "contain_access_limit": False,
            "size": 100,
            "order_field": "modify_desc",
            "language": "zh_CN",
            "dept_id": str(dept_id)
        }
        resp = requests.post(url, data=json.dumps(data))
        return ResponseParse(resp.json())

    def get_user_list_simple(self, dept_id: str = "1", next_cursor: int = 0):
        """
        获取部门员工的简单信息
        :param dept_id: 部门id
        :param next_cursor: 获取的游标开始地址
        :return: [{'name': '冯xx', 'userid': '163xxxxxxxxxxxxxxx'}]
        """
        url = "https://oapi.dingtalk.com/topapi/user/listsimple?access_token={}".format(self.access_token)
        data = {
            "cursor": next_cursor,
            "contain_access_limit": False,
            "size": 100,
            "order_field": "modify_desc",
            "language": "zh_CN",
            "dept_id": str(dept_id)
        }
        resp = requests.post(url, data=json.dumps(data))
        return ResponseParse(resp.json())

    def get_department_list(self, dept_id: str = "1"):
        """
        获取该部门下设部门的基础信息
        :param dept_id: 如果是根部门，该参数传1
        :return:[{'auto_add_user': True, 'create_dept_group': True, 'dept_id': 124000000, 'name': '测试新建', 'parent_id': 1},]
        """
        url = "https://oapi.dingtalk.com/topapi/v2/department/listsub?access_token={}".format(self.access_token)
        data = {
            "language": "zh_CN",
            "dept_id": str(dept_id)
        }
        resp = requests.post(url, data=json.dumps(data))
        return ResponseParse(resp.json())

    def get_department_list_id(self, dept_id: int = 1):
        """
        获取该部门下设部门的基础信息, 只有id信息
        :param dept_id: 如果是根部门，该参数传1
        :return:
        """
        url = "https://oapi.dingtalk.com/topapi/v2/department/listsubid?access_token={}".format(self.access_token)
        data = {
            "dept_id": str(dept_id)
        }
        resp = requests.post(url, data=json.dumps(data))
        return ResponseParse(resp.json())

    def get_all_departements_list_id(self, dept_id_list: list = [1]):
        """
        获取所有部门的id
        :param dept_id_list: 如果是根部门，该参数传['1']
        :return:
        """
        if not dept_id_list:
            return []
        ret_list = []
        for dept_id in dept_id_list:
            resp = self.get_department_list_id(dept_id)
            ret = self.get_all_departements_list_id(resp.result.get("dept_id_list"))
            ret_list = ret_list + ret
        return ret_list + dept_id_list

    def get_all_departements_list(self, dept_list: list = [{"dept_id": "1"}]):
        """
        获取所有部门的详细信息
        :param dept_list: 如果是根部门，该参数传[{"dept_id": "1"}]
        :return: [{'auto_add_user': False, 'create_dept_group': False, 'dept_id': 108510000, 'ext': '{"faceCount":"xx"}', 'name': '支撑xx', 'parent_id': 1}]
        """
        if not dept_list:
            return []
        ret_list = []
        for dept in dept_list:
            dept_id = dept.get("dept_id")
            if not dept_id: return []
            resp = self.get_department_list(dept_id)
            ret = self.get_all_departements_list(resp.result)
            ret_list = ret_list + ret
        return ret_list + dept_list

    def get_department_all_user_list(self, dept_id: int = 1):
        """
        获取该部门所有员工的基础id
        :param dept_id: 如果是根部门，该参数传1
        :return: [{
                    "leader":"true",
                    "extension":"{\"爱好\":\"旅游\",\"年龄\":\"24\"}",
                    "unionid":"z21HjQliSzpw0YWCNxmii6u2Os62cZ62iSZ",
                    "boss":"true",
                    "exclusive_account":"false",
                    "admin":"true",
                    "remark":"备注备注",
                    "title":"技术总监",
                    "hired_date":"1597573616828",
                    "userid":"zhangsan",
                    "work_place":"未来park",
                    "dept_id_list":"[2,3,4]",
                    "job_number":"4",
                    "email":"test@xxx.com",
                    "dept_order":"1",
                    "mobile":"18513027676",
                    "active":"true",
                    "telephone":"010-86123456-2345",
                    "avatar":"xxx",
                    "hide_mobile":"false",
                    "org_email":"test@xxx.com",
                    "name":"张三",
                    "state_code":"86"
                }]
        """
        ret = []
        resp = self.get_user_list(dept_id)
        ret.extend(resp.result.get("list"))
        while resp.result.get("has_more"):
            next_cursor = resp.result.get("next_cursor")
            resp = self.get_user_list(dept_id, next_cursor)
            ret.extend(resp.result.get("list"))
        return ret

    def get_department_all_user_listsimple(self, dept_id: str = "1"):
        """
        获取该部门所有员工的基础id
        :param dept_id: 如果是根部门，该参数传1
        :return:
        """
        ret = []
        resp = self.get_user_list_simple(dept_id)
        ret.extend(resp.result.get("list"))
        while resp.result.get("has_more"):
            next_cursor = resp.result.get("next_cursor")
            resp = self.get_user_list_simple(dept_id, next_cursor)
            ret.extend(resp.result.get("list"))
        return ret

    def get_all_users(self):
        """
        获取公司的全部员工信息
        :return:
        """
        dept = self.get_all_departements_list_id()
        user_list = []
        for i in dept:
            user_list.extend(self.get_department_all_user_list(i))
        return user_list

