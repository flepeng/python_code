# -*- coding:utf-8 -*-
"""
    @Time  : 2022/5/19  15:57
    @Author: Feng Lepeng
    @File  : Official.py
    @Desc  : 官方提供的示例
"""
import json
from typing import List

from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from utils.mysql import MySQLCMDB
from utils.dingtalk.self import DingTalkBase

base = DingTalkBase()
access_token = base.access_token
app_key = base.app_key


class BatchSendSingleChatMessage:
    """
    批量发送单聊消息
    https://open.dingtalk.com/document/group/chatbots-send-one-on-one-chat-messages-in-batches
    """

    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkrobot_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkrobot_1_0Client(config)

    @staticmethod
    def main(
            user_ids: List[str] = [],
            msg_key: str = 'sampleText',
            msg_param: str = "",
    ) -> None:
        """
        同步方式发送
        :param user_ids: 发送者的列表
        :param msg_key: 消息类型：https://open.dingtalk.com/document/group/message-types-and-data-format
        :param msg_param: 消息内容：json 格式
        :return:
        """
        client = BatchSendSingleChatMessage.create_client()
        batch_send_otoheaders = dingtalkrobot__1__0_models.BatchSendOTOHeaders()
        batch_send_otoheaders.x_acs_dingtalk_access_token = access_token
        batch_send_otorequest = dingtalkrobot__1__0_models.BatchSendOTORequest(
            robot_code=app_key,
            user_ids=user_ids,
            msg_key=msg_key,
            msg_param=msg_param
        )
        try:
            resp = client.batch_send_otowith_options(batch_send_otorequest, batch_send_otoheaders,
                                                     util_models.RuntimeOptions())
            print(resp)
        except Exception as err:
            print(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        client = BatchSendSingleChatMessage.create_client()
        batch_send_otoheaders = dingtalkrobot__1__0_models.BatchSendOTOHeaders()
        batch_send_otoheaders.x_acs_dingtalk_access_token = '<your access token>'
        batch_send_otorequest = dingtalkrobot__1__0_models.BatchSendOTORequest(
            robot_code='dingxxxxxx',
            user_ids=[
                'manager1234'
            ],
            msg_key='sampleMarkdown',
            msg_param='{"text": "hello text","title": "hello title"}'
        )
        try:
            await client.batch_send_otowith_options_async(batch_send_otorequest, batch_send_otoheaders,
                                                          util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


class BatchQuerySingleChatMessage:
    """
    批量查询机器人单聊消息是否已读
    https://open.dingtalk.com/document/group/chatbot-batch-query-the-read-status-of-messages
    """

    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkrobot_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkrobot_1_0Client(config)

    @staticmethod
    def main(
            process_query_key: str = ""
    ) -> None:
        """
        同步发送
        :param process_query_key: 需要查询的加密的消息 id
        :return:
        """
        client = BatchQuerySingleChatMessage.create_client()
        batch_otoquery_headers = dingtalkrobot__1__0_models.BatchOTOQueryHeaders()
        batch_otoquery_headers.x_acs_dingtalk_access_token = access_token
        batch_otoquery_request = dingtalkrobot__1__0_models.BatchOTOQueryRequest(
            robot_code=app_key,
            process_query_key=process_query_key
        )
        try:
            resp = client.batch_otoquery_with_options(batch_otoquery_request, batch_otoquery_headers,
                                               util_models.RuntimeOptions())
            print(resp)
        except Exception as err:
            print(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
            process_query_key: str = "",
    ) -> None:
        client = BatchQuerySingleChatMessage.create_client()
        batch_otoquery_headers = dingtalkrobot__1__0_models.BatchOTOQueryHeaders()
        batch_otoquery_headers.x_acs_dingtalk_access_token = '<your access token>'
        batch_otoquery_request = dingtalkrobot__1__0_models.BatchOTOQueryRequest(
            robot_code=app_key,
            process_query_key=process_query_key
        )
        try:
            await client.batch_otoquery_with_options_async(batch_otoquery_request, batch_otoquery_headers,
                                                           util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    BatchQuerySingleChatMessage.main("")

