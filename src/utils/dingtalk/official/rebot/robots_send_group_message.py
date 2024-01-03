# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/24  11:00
    @Author: Feng Lepeng
    @File  : robots_send_group_message.py
    @Desc  : 企业机器人向内部群发消息: https://open.dingtalk.com/document/group/the-robot-sends-a-group-message
"""
import sys

from typing import List

from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

from src.utils.logging_util import logger


class OrgGroupSend:
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
        access_token: str,
        msg_param: str,
        msg_key: str,
        open_conversation_id: str,
        app_key: str,
    ) -> dict:
        client = OrgGroupSend.create_client()
        org_group_send_headers = dingtalkrobot__1__0_models.OrgGroupSendHeaders()
        org_group_send_headers.x_acs_dingtalk_access_token = access_token
        org_group_send_request = dingtalkrobot__1__0_models.OrgGroupSendRequest(
            msg_param=msg_param,
            msg_key=msg_key,
            open_conversation_id=open_conversation_id,
            robot_code=app_key
        )
        try:
            resp = client.org_group_send_with_options(org_group_send_request, org_group_send_headers, util_models.RuntimeOptions())
            logger.debug(resp)
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
        client = OrgGroupSend.create_client()
        org_group_send_headers = dingtalkrobot__1__0_models.OrgGroupSendHeaders()
        org_group_send_headers.x_acs_dingtalk_access_token = '<your access token>'
        org_group_send_request = dingtalkrobot__1__0_models.OrgGroupSendRequest(
            msg_param='{"content":"今天吃肘子"}',
            msg_key='sampleText',
            open_conversation_id='cid6KeBBLoveMJOGXoYKF5x7EeiodoA==',
            robot_code='dingue4kfzdxbynxxxxxx'
        )
        try:
            await client.org_group_send_with_options_async(org_group_send_request, org_group_send_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    from sem.utils.config import conf
    from sem.utils.dingtalk.myself import ding_talk_base
    OrgGroupSend.main(
        ding_talk_base.get_access_token(),
        msg_param='{"content":"今天吃肘子"}',
        msg_key='sampleText',
        open_conversation_id=conf.DINGTALK_OPEN_CONVERSATION_ID,
        app_key=ding_talk_base.get_app_key(),
    )

