# -*- coding:utf-8 -*-
"""
    @Time  : 2022/10/12  16:38
    @Author: Feng Lepeng
    @File  : robots_send_interactive_cards.py
    @Desc  : 机器人发送互动卡片：https://open.dingtalk.com/document/group/robots-send-interactive-cards
"""
import sys

from typing import List

from alibabacloud_dingtalk.im_1_0.client import Client as dingtalkim_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.im_1_0 import models as dingtalkim__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class SendRobotInteractiveCard:
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
            access_token: str = "",
            app_key: str = "",
            args: List[str] = [],
    ) -> None:
        client = SendRobotInteractiveCard.create_client()
        send_robot_interactive_card_headers = dingtalkim__1__0_models.SendRobotInteractiveCardHeaders()
        send_robot_interactive_card_headers.x_acs_dingtalk_access_token = access_token
        send_options = dingtalkim__1__0_models.SendRobotInteractiveCardRequestSendOptions(
            at_user_list_json='[{"nickName":"张三","userId":"userId0001"},{"nickName":"李四","unionId":"unionId001"}]',
            # 消息@人。
            at_all=False,  # 是否@所有人。
            receiver_list_json='[{"userId":"userId0001"},{"unionId":"unionId001"}]',  # 消息仅部分人可见的接收人列表。
            card_property_json='{}'  # 卡片特殊属性json字符串。
        )
        send_robot_interactive_card_request = dingtalkim__1__0_models.SendRobotInteractiveCardRequest(
            card_template_id='ab6a7fb9-1dd3-458c-8000-de1f7ffd0e51',  # 互动卡片的消息模板ID
            # open_conversation_id='cidXXXX',  # 接收卡片的加密群ID，特指多人群会话（非单聊）, openConversationId和singleChatReceiver 二选一必填。
            single_chat_receiver='{"userId":"163560584720757486"}',  # 单聊会话接收者json串
            card_biz_id='cardXXXX01',  # 唯一标识一张卡片的外部ID，卡片幂等ID，可用于更新或重复发送同一卡片到多个群会话
            robot_code=app_key,  # 企业内部开发-机器人为机器人应用appKey。
            # callback_url='https://***',  # 可控制卡片回调的URL，不填则无需回调。
            # 钉钉卡片是通过 JSON 数据结构进行描述的，总共可将该描述划分为三个部分：卡片属性、卡片头部以及卡片内容。
            card_data="""  
            {
                "config": {
                    "autoLayout": true,
                    "enableForward": true
                },
                "header": {
                    "title": {
                        "type": "text",
                        "text": "钉钉卡片测试"
                    },
                    "logo": "@lALPDfJ6V_FPDmvNAfTNAfQ"
                },
                "contents": [
                    {
                        "type": "text",
                        "text": "bucket 下载申请",
                        "id": "title"
                    },
                ]
            }
            """,

            # user_id_private_data_map='{"userId0001":{"xxxx":"xxxx"}}',  # 卡片模板userId差异用户参数，json结构体。
            # union_id_private_data_map='{"unionId0001":{"xxxx":"xxxx"}}',  # 卡片模板unionId差异用户参数，json结构体。
            # send_options=send_options,
            pull_strategy=False  # 是否开启卡片纯拉模式
        )
        try:
            client.send_robot_interactive_card_with_options(send_robot_interactive_card_request,
                                                            send_robot_interactive_card_headers,
                                                            util_models.RuntimeOptions())
        except Exception as err:
            print(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                print(err.code, err.message)

    @staticmethod
    async def main_async(
            args: List[str],
    ) -> None:
        client = SendRobotInteractiveCard.create_client()
        send_robot_interactive_card_headers = dingtalkim__1__0_models.SendRobotInteractiveCardHeaders()
        send_robot_interactive_card_headers.x_acs_dingtalk_access_token = '<your access token>'
        send_options = dingtalkim__1__0_models.SendRobotInteractiveCardRequestSendOptions(
            at_user_list_json='[{"nickName":"张三","userId":"userId0001"},{"nickName":"李四","unionId":"unionId001"}]',
            at_all=False,
            receiver_list_json='[{"userId":"userId0001"},{"unionId":"unionId001"}]',
            card_property_json='{}'
        )
        send_robot_interactive_card_request = dingtalkim__1__0_models.SendRobotInteractiveCardRequest(
            card_template_id='xxxxxxxx',
            open_conversation_id='cidXXXX',
            single_chat_receiver='以userId为例：{"userId":"userId0001"}；以unionId为例{"unionId":"unionId001"}',
            card_biz_id='cardXXXX01',
            robot_code='xxxxxx',
            callback_url='https://***',
            card_data='{   "config": {     "autoLayout": true,     "enableForward": true   },   "header": {     "title": {       "type": "text",       "text": "钉钉卡片"     },     "logo": "@lALPDfJ6V_FPDmvNAfTNAfQ"   },   "contents": [     {       "type": "text",       "text": "钉钉正在为各行各业提供专业解决方案，沉淀钉钉1900万企业组织核心业务场景，提供专属钉钉、教育、医疗、新零售等多行业多维度的解决方案。",       "id": "text_1658220665485" } ]}',
            user_id_private_data_map='{"userId0001":{"xxxx":"xxxx"}}',
            union_id_private_data_map='{"unionId0001":{"xxxx":"xxxx"}}',
            send_options=send_options,
            pull_strategy=False
        )
        try:
            await client.send_robot_interactive_card_with_options_async(send_robot_interactive_card_request,
                                                                        send_robot_interactive_card_headers,
                                                                        util_models.RuntimeOptions())
        except Exception as err:
            if not UtilClient.empty(err.code) and not UtilClient.empty(err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    from sem.utils.config import conf
    from sem.utils.dingtalk.myself import DingTalkBase

    base = DingTalkBase(conf.DINGTALK_APP_KEY, conf.DINGTALK_APP_SECRET)
    access_token = base.get_access_token()
    app_key = base.app_key
    SendRobotInteractiveCard.main(access_token, app_key)
