# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/12  15:28
    @Author: Feng Lepeng
    @File  : batch_query_single_chat_message.py
    @Desc  : 批量查询机器人单聊消息是否已读
                https://open.dingtalk.com/document/group/chatbot-batch-query-the-read-status-of-messages
"""
from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from src.utils.logging_util import logger


class BatchOTOQuery:

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
            process_query_key: str = "",
            app_key: str = "",
            access_token: str = ""
    ) -> None:
        """
        同步发送
        :param process_query_key: 需要查询的加密的消息 id
        :param app_key: app_key
        :param access_token: access_token
        :return:
        """
        client = BatchOTOQuery.create_client()
        batch_otoquery_headers = dingtalkrobot__1__0_models.BatchOTOQueryHeaders()
        batch_otoquery_headers.x_acs_dingtalk_access_token = access_token
        batch_otoquery_request = dingtalkrobot__1__0_models.BatchOTOQueryRequest(
            robot_code=app_key,
            process_query_key=process_query_key
        )
        try:
            resp = client.batch_otoquery_with_options(batch_otoquery_request, batch_otoquery_headers,
                                               util_models.RuntimeOptions())
            logger.debug(resp)
        except Exception as err:
            logger.exception(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
            process_query_key: str = "",
            app_key: str = ""
    ) -> None:
        client = BatchOTOQuery.create_client()
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


