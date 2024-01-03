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
from utils.ini_util import conf


class ResponseParse():

    def __init__(self, data):
        self.err_code = data.get("errcode")
        self.err_msg = data.get("errmsg")
        self.request_id = data.get("request_id")
        self.result = data.get("result")
        if self.err_code:
            print(data)
            raise KeyError("发生错误")


class DingTalkBase(object):
    """
    获取 access token
    """

    def __init__(self, app_key: str, app_secret: str):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = ""
        self.last_get_timestamp = 0

    def __get_access_token_from_dingtalk(self):
        """
        获取 access token
        :return:
        """
        url = "https://oapi.dingtalk.com/gettoken?appkey={}&appsecret={}".format(self.app_key, self.app_secret)
        resp = requests.get(url)
        if resp.json().get("errcode") == 0:
            self.access_token = resp.json().get("access_token")
            self.last_get_timestamp = time.time()
            return
        raise KeyError("发生错误")

    def get_access_token(self):
        if time.time() - self.last_get_timestamp > 7000:
            self.__get_access_token_from_dingtalk()
        return self.access_token

    def get_app_key(self):
        return self.app_key


class DingTalk(DingTalkBase):

    def __init__(self, app_key: str, app_secret: str):
        super().__init__(app_key, app_secret)
        self.webhook = ""
        self.sign = ""
        self.headers = {'Content-Type': 'application/json; charset=utf-8'}
        self.times = 0
        self.single_chat_url = "/v1.0/robot/oToMessages/batchSend"
        self.user_list = []
        self.dept_id_list = [
            469890217, 469854248, 470304064, 470173083, 469916201, 475662415, 484646128, 503123846,
            470260061, 470186089, 469989194, 469978130, 550047304, 469052993, 469905208, 396701474,
            305875441, 366794646, 493997019, 322021373, 399721727, 486117544, 391394241, 558894502,
            407234930, 387342285, 414715620, 410907971, 561135276, 503569125, 503584098, 503595085,
            577417710, 577199749, 426311497, 469914246, 450491420, 469952165, 469793322, 558544934,
            73695179, 470389030, 418248345, 574303727, 418515689, 470124089, 592871370, 124550033,
            399544333, 543592379, 469933181, 577027867, '1']

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

    def get_user_listsimple(self, dept_id: str = "1", next_cursor: int = 0):
        """
        获取部门员工的简单信息
        :param dept_id: 部门id
        :param next_cursor: 获取的游标开始地址
        :return: [{'name': '冯乐鹏', 'userid': '163560584720757486'}]
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
        :return:[{'auto_add_user': True, 'create_dept_group': True, 'dept_id': 124550033, 'name': '测试新建', 'parent_id': 1}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 73695179, 'name': 'IT', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 399544333, 'name': '测试项目', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 418248345, 'name': '测试部门', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 418515689, 'name': '钉钉工作台', 'parent_id': 1}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 426311497, 'name': 'data 实习生', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 450491420, 'name': '算法开发产品部', 'parent_id': 1}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 469793322, 'name': 'CFO线', 'parent_id': 1, 'source_identifier': '-----F----.LOqKuF:2:449093209'}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 469914246, 'name': '企业业务事业部', 'parent_id': 1, 'source_identifier': '-----F----.LOqKuF:2:448484531'}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 469933181, 'name': 'CTO线', 'parent_id': 1}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 469952165, 'name': 'CEO线', 'parent_id': 1, 'source_identifier': '-----F----.LOqKuF:2:448879372'}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 470124089, 'name': 'COO线', 'parent_id': 1, 'source_identifier': '-----F----.LOqKuF:2:448769501'}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 470389030, 'name': '总裁线', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 543592379, 'name': '不隐藏部门', 'parent_id': 1}, {'auto_add_user': False, 'create_dept_group': False, 'dept_id': 558544934, 'name': 'CHO线', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 574303727, 'name': '测试测试', 'parent_id': 1}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 577027867, 'name': '云服务事业部', 'parent_id': 1, 'source_identifier': '-----F----.LOqKuF:2:450360384'}, {'auto_add_user': True, 'create_dept_group': True, 'dept_id': 592871370, 'name': '安全部', 'parent_id': 1}]
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

    def get_all_departements_id(self, dept_id_list: list = ['1']):
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
            ret = self.get_all_departements_id(resp.result.get("dept_id_list"))
            ret_list = ret_list + ret
        return ret_list + dept_id_list

    def get_all_departements(self, dept_list: list = [{"dept_id": "1"}]):
        """
        获取所有部门的详细信息
        :param dept_list: 如果是根部门，该参数传[{"dept_id": "1"}]
        :return: [{'auto_add_user': False, 'create_dept_group': False, 'dept_id': 108516xxx, 'ext': '{"faceCount":"xx"}', 'name': '支撑xx', 'parent_id': 1}]
        """
        if not dept_list:
            return []
        ret_list = []
        for dept in dept_list:
            dept_id = dept.get("dept_id")
            if not dept_id: return []
            resp = self.get_department_list(dept_id)
            ret = self.get_all_departements(resp.result)
            ret_list = ret_list + ret
        return ret_list + dept_list

    def get_department_all_user_list(self, dept_id: str = "1"):
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
        resp = self.get_user_listsimple(dept_id)
        ret.extend(resp.result.get("list"))
        while resp.result.get("has_more"):
            next_cursor = resp.result.get("next_cursor")
            resp = self.get_user_listsimple(dept_id, next_cursor)
            ret.extend(resp.result.get("list"))
        return ret

    def get_all_users_id(self):
        dept = [641459137, 612471709, 640967481, 612426756, 479289582, 478898835, 695919294, 373881184, 381129559, 373930121, 381282431, 496111407, 541870416, 400831612, 421123687, 620924870, 620767925, 399706294, 695943240, 373679921, 431365698, 542263461, 400631913, 621009739, 399377383, 63938414, 76367052, 79431423, 79426239, 58288625, 57702170, 57702202, 57702203, 57702172, 57702177, 74885447, 77727057, 65957817, 93942001, 99120111, 99047168, 67316610, 77951171, 74795266, 66753617, 84857068, 84953087, 99029190, 57414463, 70831233, 99247139, 90596236, 57414464, 57414465, 84922082, 73549036, 57343215, 504712167, 504733142, 450310339, 450201336, 450191416, 369453931, 587788336, 354410485, 503916071, 470576160, 468532128, 514261517, 486798272, 468460137, 514130782, 355006459, 108976025, 105534631, 108802116, 364058519, 123488066, 123319103, 151241609, 108916113, 133286687, 99264133, 354194956, 468477118, 354875503, 93838125, 93596681, 364023679, 99208119, 369804008, 58018224, 370537399, 103529372, 108781193, 98900077, 380453974, 103350296, 132505270, 94908060, 99261111, 103517466, 99029191, 145987954, 99135179, 379802400, 133269189, 300816136, 659597019, 99135184, 108843076, 94886061, 99044170, 99044168, 99111149, 108677775, 344750232, 417496128, 370365769, 416843938, 393883262, 393591954, 393654971, 393682768, 547407670, 478251117, 483787289, 548156061, 477822265, 482799971, 505020150, 505153051, 499731286, 477717339, 499698282, 343212462, 343403101, 551462826, 551670719, 489185219, 485642338, 489812055, 475980202, 477627200, 475821306, 477744083, 481671157, 481984083, 595910459, 485395455, 475771296, 478931894, 149246314, 85161021, 129986823, 592560281, 357788686, 365133442, 349783957, 149251222, 644591677, 84876919, 129970865, 349958277, 533192521, 103408411, 103364396, 103570305, 85212005, 118466184, 118460291, 533153543, 118274585, 134904790, 135017246, 113218362, 113231256, 113135399, 113172277, 135017245, 112967069, 68989812, 103599377, 103642333, 103423352, 103562391, 99228122, 99086150, 99168148, 99208118, 108767322, 108610596, 108955224, 104712291, 103509284, 99029185, 99180118, 99015144, 99101143, 108950092, 70818178, 108596957, 108580915, 108654701, 103348465, 108541841, 70823153, 99192137, 99202140, 99170143, 103516438, 103495349, 103396371, 119796560, 103589481, 119751618, 99111147, 99058139, 124590069, 99255123, 99255120, 124415108, 113116520, 99170142, 99015148, 113054455, 103634297, 108735655, 103372326, 103378516, 196778715, 99058128, 467716264, 99153132, 99142125, 108767324, 128383249, 433479277, 131044463, 99244152, 86050357, 108658720, 99184119, 99193111, 103640396, 103393328, 103452428, 129270295, 83318115, 129307152, 166728331, 166774205, 166691521, 166809096, 351766634, 515889798, 292867391, 434789614, 515920683, 166647822, 351904525, 291997825, 84997971, 118506229, 113153256, 78691130, 83389109, 166613728, 545894584, 546063419, 409532308, 492118178, 507165917, 498125594, 484910729, 492026290, 485188258, 146913232, 146914115, 543939143, 656098975, 478302699, 641654198, 426391027, 426223209, 545236730, 409066547, 652100630, 543835187, 477913649, 426299110, 545710568, 408714675, 562427958, 475968370, 500754350, 703779473, 476265159, 500919214, 482830521, 492027443, 482749532, 488376465, 498509291, 475326307, 475352156, 583330665, 488540350, 498663308, 475437151, 584189435, 612211708, 478800747, 373626945, 551382488, 504553524, 108687677, 471183292, 108516604, 342538657, 370596219, 58102278, 393667751, 477884170, 612908668, 475779299, 108637696, 409492371, 484943515, 146911164, 408886850, 476471131, 482365982, 475420169, '1']

        pass


ding_talk_base = DingTalkBase(conf.DINGTALK_APP_KEY, conf.DINGTALK_APP_SECRET)
ding_talk_base_outsouring = DingTalkBase(conf.DINGTALK_APP_KEY_OUTSOURING, conf.DINGTALK_APP_SECRET_OUTSOURIN)


if __name__ == "__main__":
    # print(DingTalk(conf.DINGTALK_APP_KEY, conf.DINGTALK_APP_SECRET).get_department_list("592871370").result)
    print(DingTalk(conf.DINGTALK_APP_KEY, conf.DINGTALK_APP_SECRET).get_department_all_user_list("592871370"))

