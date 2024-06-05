# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/12  14:04
    @Author: Feng Lepeng
    @File  : robots_send_interactive_cards_update.py
    @Desc  : 更新机器人发送互动卡片: https://open.dingtalk.com/document/group/update-the-robot-to-send-interactive-cards
"""
import sys

from typing import List

from alibabacloud_dingtalk.im_1_0.client import Client as dingtalkim_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.im_1_0 import models as dingtalkim__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class UpdateRobotInteractiveCardRequest:
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
            app_key: str = "",
            access_token: str = ""
    ) -> None:
        client = UpdateRobotInteractiveCardRequest.create_client()
        update_robot_interactive_card_headers = dingtalkim__1__0_models.UpdateRobotInteractiveCardHeaders()
        update_robot_interactive_card_headers.x_acs_dingtalk_access_token = access_token
        update_options = dingtalkim__1__0_models.UpdateRobotInteractiveCardRequestUpdateOptions(
            update_card_data_by_key=False,
            update_private_data_by_key=False
        )
        update_robot_interactive_card_request = dingtalkim__1__0_models.UpdateRobotInteractiveCardRequest(
            card_biz_id='cardXXXX01',
            card_data='根据具体的cardTemplateId参考文档格式',
            user_id_private_data_map='{"userId0001":{"xxxx":"xxxx"}}',
            union_id_private_data_map='{"unionId0001":{"xxxx":"xxxx"}}',
            update_options=update_options
        )
        try:
            client.update_robot_interactive_card_with_options(update_robot_interactive_card_request, update_robot_interactive_card_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass

    @staticmethod
    async def main_async(
        args: List[str],
    ) -> None:
        client = UpdateRobotInteractiveCardRequest.create_client()
        update_robot_interactive_card_headers = dingtalkim__1__0_models.UpdateRobotInteractiveCardHeaders()
        update_robot_interactive_card_headers.x_acs_dingtalk_access_token = '<your access token>'
        update_options = dingtalkim__1__0_models.UpdateRobotInteractiveCardRequestUpdateOptions(
            update_card_data_by_key=False,
            update_private_data_by_key=False
        )
        update_robot_interactive_card_request = dingtalkim__1__0_models.UpdateRobotInteractiveCardRequest(
            card_biz_id='cardXXXX01',
            card_data='根据具体的cardTemplateId参考文档格式',
            user_id_private_data_map='{"userId0001":{"xxxx":"xxxx"}}',
            union_id_private_data_map='{"unionId0001":{"xxxx":"xxxx"}}',
            update_options=update_options
        )
        try:
            await client.update_robot_interactive_card_with_options_async(update_robot_interactive_card_request, update_robot_interactive_card_headers, util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    UpdateRobotInteractiveCardRequest.main()

