# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/25  10:24
    @Author: Feng Lepeng
    @File  : test.py
    @Desc  :
"""
import json

from utils.mysql import MySQLLocal
from utils.dingtalk.official.rebot import BatchSendOTO
from utils.dingtalk.myself import ding_talk_base


def read_xlsx():
    import pandas as pd

    data = pd.read_excel("13.xlsx", sheet_name="Sheet2")
    ret = data["账号"].values
    user_list = [i for i in ret]
    sql = "select dingding_id from company_dingding where user_code in {}".format(tuple(user_list))
    ret = MySQLLocal().select(sql)
    ret = [i[0] for i in ret]
    return ret


def get_all_user_dingtalk():
    dict_user_dingtalk = {}
    sql = """
    select a.userCode,b.dingding_id from company_info a 
left join company_dingding b on a.userCode=b.user_code
where a.status='1' and b.dingding_id is not NULL and dingding_id != ''
    """
    ret = MySQLLocal().select(sql)
    for i in ret:
        dict_user_dingtalk[i[0]] = i[1]
    return dict_user_dingtalk


class DingTalkSendMsg():

    def send_msg(self, user_ids, test):

        start_num = 0

        print(len(user_ids), user_ids)

        while start_num < len(user_ids):
            # &nbsp; 空行
            # &emsp;

            # msg_param = json.dumps({"content": test, "title": "WPS office办公套件升级通知"})
            msg_param = json.dumps({"text": test, "title": "安全通知"})
            BatchSendOTO.main(
                user_ids=user_ids[start_num: start_num + 100],
                msg_param=msg_param,
                msg_key="sampleMarkdown",
                app_key=ding_talk_base.get_app_key(),
                access_token=ding_talk_base.get_access_token()
            )

            start_num += 100

    def send_bucket_unlabeled(self, user_dingtalk):

        with open("111.json") as f:
            for line in f.readlines():
                data = json.loads(line.strip())
                owner = data.get("result").get("owner")
                values = data.get("result").get("name")

                if type(values) == str:
                    bucket_str = "1. {}\r\n".format(values)
                else:
                    bucket_str = ""
                    num = 1
                    for i in values:
                        bucket_str = bucket_str + "{}. {}\r\n".format(num, i)
                        num += 1

                if user_dingtalk.get(owner):
                    # print(owner, user_dingtalk.get(owner))
                    test = """aaaaaaaaa""".format(bucket_str)
                    # print(test)
                    self.send_msg([user_dingtalk.get(owner)], test)
                else:
                    print("没有找到" + owner)
                # exit()

    def send_bucket_high_level(self, user_dingtalk):

        with open("high_level.json", encoding="utf-8") as f:
            for line in f.readlines():
                data = json.loads(line.strip())
                owner = data.get("result").get("owner")
                values = data.get("result").get("values(bucket)")

                if type(values) == str:
                    bucket_str = "1. {}\r\n".format(values)
                else:
                    bucket_str = ""
                    num = 1
                    for i in values:
                        bucket_str = bucket_str + "{}. {}\r\n".format(num, i)
                        num += 1

                if user_dingtalk.get(owner):
                    print(owner, user_dingtalk.get(owner))
                    test = """bbbbbbbbb""".format(bucket_str)
                    self.send_msg([user_dingtalk.get(owner)], test)
                else:
                    print("没有找到" + owner)
                # exit()

    def send_bucket_action_card(self):

        start_num = 0

        user_ids = [
            "163560584720757486",  # fenglepeng
            # "225315361139140174",   # gaoshenghan
            # "061367526135489858",   # zhaohuatao
            "062541521921189223"    # liuchengjian
        ]
        test = "![这是一张图片](https://img.alicdn.com/tfs/TB1NwmBEL9TBuNjy1zbXXXpepXa-2400-1218.png) \n  这是一个整体跳转actionCard消息"

        while start_num < len(user_ids):
            # &nbsp; 空行
            # &emsp;

            # msg_param = json.dumps({"content": test, "title": "WPS office办公套件升级通知"})
            msg_param = json.dumps({
                "title": "独立跳转actionCard消息",
                "text": test,
                "buttonTitle1": "查看摘要",
                # "buttonUrl1": "http://81.70.160.146:8080",
                "buttonUrl1": "https://open.dingtalk.com/document/",
                "buttonTitle2": "不感兴趣",
                "buttonUrl2": "https://open.dingtalk.com/",
                "btns": [
                    {
                        "title": "查看摘要",
                        "actionURL": "https://open.dingtalk.com/document/"
                    },
                    {
                        "title": "不感兴趣",
                        "actionURL": "https://open.dingtalk.com/"
                    }
                ]
            })
            BatchSendOTO.main(
                user_ids=user_ids[start_num: start_num + 100],
                msg_param=msg_param,
                msg_key="sampleActionCard6",
                app_key=ding_talk_base.get_app_key(),
                access_token=ding_talk_base.get_access_token()
            )

            start_num += 100


if __name__ == '__main__':
    user_dingtalk = get_all_user_dingtalk()
    ret = DingTalkSendMsg().send_bucket_unlabeled(user_dingtalk)

    # a = "qy1t/buOEheUrCLXV2Ll2OXo64C8Eszcc0N1QYpfAJ4="
    # a = "seMqYgsi9VZDpDHyAakl1MTi0XnRuYKKZMrtGonWK+o="
    # a = "1TRiO005MJCBZoV1PYKtdnsHmFv8atwt8ptzutzxDZk="




