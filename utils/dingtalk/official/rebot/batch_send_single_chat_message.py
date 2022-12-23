# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/12  15:26
    @Author: Feng Lepeng
    @File  : batch_send_single_chat_message.py
    @Desc  : 批量发送单聊消息官方代码
               https://open.dingtalk.com/document/group/chatbots-send-one-on-one-chat-messages-in-batches
"""
import json
from typing import List

from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from utils.logging import logger


class BatchSendOTO:

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
            app_key: str = "",
            access_token: str = ""
    ) -> dict:
        """
        同步方式发送
        :param user_ids: 发送者的列表
        :param msg_key: 消息类型：https://open.dingtalk.com/document/group/message-types-and-data-format
        :param msg_param: 消息内容：json 格式
        :param app_key: app_key
        :param access_token: access_token
        :return:
        """
        client = BatchSendOTO.create_client()
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

            """
            resp示例：{
                'flowControlledStaffIdList': [],  # 被限流的userid列表
                'invalidStaffIdList': [],  # 无效的用户userid列表
                'processQueryKey': 'rZoxzOUAVDSEovnYDm5UC0oAZ0+yLN196q9PEDba8mQ='  # 消息id。
            }
            """
            return {"code": "200", "message": str(resp.body)}
        except Exception as err:
            logger.exception(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                return {"code": "400", "message": err.message}

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        client = BatchSendOTO.create_client()
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

