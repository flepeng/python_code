# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/24  11:34
    @Author: Feng Lepeng
    @File  : get_group_openconversationid.py
    @Desc  : 获取群会话的OpenConversationId: https://open.dingtalk.com/document/orgapp-server/obtain-group-openconversationid
"""
from typing import List

from alibabacloud_dingtalk.im_1_0.client import Client as dingtalkim_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.im_1_0 import models as dingtalkim__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class ChatIdToOpenConversationId:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkim_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkim_1_0Client(config)

    @staticmethod
    def main(
        access_token: str,
        chat_id: str
    ) -> None:
        client = ChatIdToOpenConversationId.create_client()
        chat_id_to_open_conversation_id_headers = dingtalkim__1__0_models.ChatIdToOpenConversationIdHeaders()
        chat_id_to_open_conversation_id_headers.x_acs_dingtalk_access_token = access_token
        try:
            ret = client.chat_id_to_open_conversation_id_with_options(chat_id, chat_id_to_open_conversation_id_headers, util_models.RuntimeOptions())
            print(ret)
        except Exception as err:
            print(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = ChatIdToOpenConversationId.create_client()
        chat_id_to_open_conversation_id_headers = dingtalkim__1__0_models.ChatIdToOpenConversationIdHeaders()
        chat_id_to_open_conversation_id_headers.x_acs_dingtalk_access_token = '<your access token>'
        try:
            await client.chat_id_to_open_conversation_id_with_options_async('chatfaabe59a460527f5fb72fbbdfe3f061e', chat_id_to_open_conversation_id_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    from sem.utils.dingtalk.myself import ding_talk_base
    print(ding_talk_base.get_access_token())

    ChatIdToOpenConversationId.main(ding_talk_base.get_access_token(), "")

