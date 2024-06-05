# -*- coding: utf-8 -*-


import time
import random
import logging

import csv
import requests

logger = logging.getLogger()


class Main(object):

    def __init__(self):
        self.keywords = ["喜茶"]
        # self.url = "https://www.douyin.com/search/%s?aid=76dfeef6-3fd1-4071-afe8-113ebcf170fa&publish_time=0&sort_type=0&source=normal_search&type=general"
        self.search_url = "https://www.douyin.com/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&sort_type=0&publish_time=0&keyword=%s&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&offset=%s&count=10&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=108.0.0.0&browser_online=true&engine_name=Blink&engine_version=108.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7173207302987089420&msToken=8WnGTYL7gOc3b1tFp213dOiZ3V7xB-nP8XA2ZCxFFLSb2f019iMmlMtS7pCuYkkYTqSAjJywQyQnFkscspf5I3IcYtWFzXpqhKsxFNYpOiAR2xGXSJik&X-Bogus=DFSzswVYxUXANt1kSDcsCr7TlqSZ"
        self.comment_url = "https://www.douyin.com/aweme/v1/web/comment/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&aweme_id=%s&cursor=%s&count=%s&item_type=0&insert_ids=&rcFT=&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=108.0.0.0&browser_online=true&engine_name=Blink&engine_version=108.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7173207302987089420&msToken=R-KBD9-LRxzRFuIr07Fh_ayrTugGpUlpiONld7uLPwA9guBOmREjMPQqdt6365ykel3LBO4x-BMOAnCQy9oHBSbBVx8vVpcy8P6xuEaGhfO738MEZSSi&X-Bogus=DFSzswVuRd2ANCohSDcvr37TlqS3"
        self.remark_url = "https://www.douyin.com/aweme/v1/web/comment/list/reply/?device_platform=webapp&aid=6383&channel=channel_pc_web&item_id=%s&comment_id=%s&cursor=%s&count=%s&item_type=0&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=108.0.0.0&browser_online=true&engine_name=Blink&engine_version=108.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7173207302987089420&msToken=XvSI_hDZ25VHDcXXT6-SdXAeAfOeYdP8yeZO9f3_Y_WxS6lkJkzGXPYUUKSccT9I5uGzTr2_VJKQh6YLiYe501cQS9cZj-wtNdQg9f_TcsNdfD5df2he&X-Bogus=DFSzswVuSb2ANCohSDcWcN7Tlqe-"

        self.v_off = 0
        self.video_file_name = "Video"
        self.comment_file_name = "Comment"

        f = open(f"{self.video_file_name}.csv", "w+")
        csv_obj = csv.writer(f)
        titles = ["博主名", "博主抖音号", "视频ID", "发布时间", "视频标题",
                  "分享链接", "评论数", "点赞数", "分享数"]
        csv_obj.writerow(titles)
        f.close()

        f = open(f"{self.comment_file_name}.csv", "w+")
        csv_obj = csv.writer(f)
        titles = ["视频ID", "点赞数", "回复数", "评论内容"]
        csv_obj.writerow(titles)
        f.close()

    def __request(self, method: str, url, *args, **kwargs):
        headers = kwargs.get("headers", {})
        headers.update(self.default_headers)
        # headers[":path"] = url
        res = getattr(requests, method, None)
        if not res:
            print("Requests err. not mothod. %s" % method)
            raise

        try:
            resp = res(url, headers=headers, *args, **kwargs)
            print(resp.status_code)
            print(resp.content)
            print(resp.text)
            print(resp.json())

            if resp.status_code == 200:
                return resp.json()
            print("Requests err. Http status is %s" % resp.status_code)
        except Exception as e:
            logger.exception("__request error.")
        return

    def list_video(self, keyword: str = "", offset: int = 0, limit: int = 10) -> list:
        time.sleep(random.randrange(1, 2))
        url = self.search_url % (keyword, offset)
        res = self.__request("get", url)
        print(res["data"])
        if not res or res.get("status_code") != 0:
            return []
        # self.v_off = res.get("cursor") or self.v_off + 10
        return res["data"]

    def list_comment(self, aweme_id: str = None, comment_id: str = None, offset: int = 0, limit: int = 20):
        print("query comments", aweme_id, comment_id, offset)
        if comment_id:
            url = self.remark_url % (aweme_id, comment_id, offset, limit)
        else:
            url = self.comment_url % (aweme_id, offset, limit)
        print(url)
        res = self.__request("get", url)
        exit()
        if not res or res.get("status_code") != 0:
            return []
        return res

    def login(self):
        time.sleep(0.5)

    def start(self):
        print(">> starting")
        for i in self.keywords:
            for j in range(20):
                videos: list = self.list_video(i, j * 10)
                for v_data in videos:
                    try:
                        self.handle_video(v_data)
                    except Exception as e:
                        logger.exception(e)
                        # print(v_data)

    @property
    def default_headers(self):
        _headers = {
            # ":authority": "www.douyin.com",
            # ":method": "GET",
            # ":path": "/aweme/v1/web/general/search/single/?device_platform=webapp&aid=6383&channel=channel_pc_web&search_channel=aweme_general&sort_type=0&publish_time=0&keyword=%E5%A5%88%E9%9B%AA&search_source=normal_search&query_correct_type=1&is_filter_search=0&from_group_id=&offset=0&count=10&pc_client_type=1&version_code=170400&version_name=17.4.0&cookie_enabled=true&screen_width=1440&screen_height=900&browser_language=zh-CN&browser_platform=MacIntel&browser_name=Chrome&browser_version=108.0.0.0&browser_online=true&engine_name=Blink&engine_version=108.0.0.0&os_name=Mac+OS&os_version=10.15.7&cpu_core_num=8&device_memory=8&platform=PC&downlink=10&effective_type=4g&round_trip_time=50&webid=7173207302987089420&msToken=8WnGTYL7gOc3b1tFp213dOiZ3V7xB-nP8XA2ZCxFFLSb2f019iMmlMtS7pCuYkkYTqSAjJywQyQnFkscspf5I3IcYtWFzXpqhKsxFNYpOiAR2xGXSJik&X-Bogus=DFSzswVYxUXANt1kSDcsCr7TlqSZ"
            # ":scheme": "https",
            "accept": "application/json, text/plain, */*",
            # "accept-encoding": "gzip, deflate, br",
            "accept-encoding": "gzip, deflate",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "ttwid=1%7CLdXi0sL0_ft9JF-1fEl3cB15HZV_Cn-yxEEP3KE84CA%7C1670142491%7C8fd13ec11292f7ccade72d2284a738efde7c81e17fd2a717e4857bc9b0cbc4ce; douyin.com; home_can_add_dy_2_desktop=%220%22; passport_csrf_token=dbd3c1d732df23165f6149e826cb3a5a; passport_csrf_token_default=dbd3c1d732df23165f6149e826cb3a5a; ttcid=2a2ffa6d03f248b9a7af4135f1bbbfd418; SEARCH_RESULT_LIST_TYPE=%22single%22; s_v_web_id=verify_lcmw2f5i_3T3LDDUn_XwR6_4gwD_8GEX_5mhTjmMu2T2k; download_guide=%223%2F20230108%22; passport_assist_user=CjwjZqKF9ZCUfex1VbiJNvh51lrGzydhrA8kF_DR1Tb8dz_TfApLlDAb5pGrcqTU_zHNRZDvQp7nl9KI7RYaSAo8tlZtxb8tmpN7umHnwre1NPsPhuF5ZmTFWVZSBwnpRYs5tHS8uoJJGHdiaRwSnMuz7Gv5DxRAlIGp948MENmBpg0Yia_WVCIBA4ivYgg%3D; n_mh=5NlVlke-bgEFRCKhi_81sn7xsY2LI4PXI-VkTyoJ1J4; sso_uid_tt=746b18993186c71ad7f08ba866d15904; sso_uid_tt_ss=746b18993186c71ad7f08ba866d15904; toutiao_sso_user=813b9dc4485f04db4b04553147f1a106; toutiao_sso_user_ss=813b9dc4485f04db4b04553147f1a106; sid_ucp_sso_v1=1.0.0-KDM0Y2YwOTgxYzliYjg3Y2U3MzVkNjE3Mzk5MzMwMmZiMWE3ODQ0MDkKHQi7vYrQ2gIQoLrpnQYY7zEgDDCJho7UBTgGQPQHGgJscSIgODEzYjlkYzQ0ODVmMDRkYjRiMDQ1NTMxNDdmMWExMDY; ssid_ucp_sso_v1=1.0.0-KDM0Y2YwOTgxYzliYjg3Y2U3MzVkNjE3Mzk5MzMwMmZiMWE3ODQ0MDkKHQi7vYrQ2gIQoLrpnQYY7zEgDDCJho7UBTgGQPQHGgJscSIgODEzYjlkYzQ0ODVmMDRkYjRiMDQ1NTMxNDdmMWExMDY; odin_tt=dfca98852a06daf45a0c97b65c8fe555c264c78a90ead94091f47f5a2c959e108bb92fde44d1fad4c8510728bf430b85; passport_auth_status=b6651e0cd834cb178a143fca2a60fc04%2C; passport_auth_status_ss=b6651e0cd834cb178a143fca2a60fc04%2C; uid_tt=f739c4ecc5800679cb64669c9eccdd9d; uid_tt_ss=f739c4ecc5800679cb64669c9eccdd9d; sid_tt=9c70d71ec7c4df7ac2c4aa9c04604970; sessionid=9c70d71ec7c4df7ac2c4aa9c04604970; sessionid_ss=9c70d71ec7c4df7ac2c4aa9c04604970; _tea_utm_cache_2018=undefined; sid_guard=9c70d71ec7c4df7ac2c4aa9c04604970%7C1673157957%7C5183962%7CThu%2C+09-Mar-2023+06%3A05%3A19+GMT; sid_ucp_v1=1.0.0-KDVmOWVlNWIwN2ExZTg3OTQwNGFmYzcwZGI3ODA4YzM3MGE0ZjliZGMKFwi7vYrQ2gIQxbrpnQYY7zEgDDgGQPQHGgJobCIgOWM3MGQ3MWVjN2M0ZGY3YWMyYzRhYTljMDQ2MDQ5NzA; ssid_ucp_v1=1.0.0-KDVmOWVlNWIwN2ExZTg3OTQwNGFmYzcwZGI3ODA4YzM3MGE0ZjliZGMKFwi7vYrQ2gIQxbrpnQYY7zEgDDgGQPQHGgJobCIgOWM3MGQ3MWVjN2M0ZGY3YWMyYzRhYTljMDQ2MDQ5NzA; csrf_session_id=a775fabb983766fdeb96f6229a48ce5a; __ac_signature=_02B4Z6wo00f01tvMSLgAAIDBTxoTtZ71Eerb7EwAANVWpMv3gGiuJGqUMnEheAhHPhxreW1Dz0lP0KSind9mu6Drf0TP9.MGxCpAvVWFpW2Wzayehv48IJqJXGM45diwi2PS2sW-2xh39A7.56; LOGIN_STATUS=1; FOLLOW_LIVE_POINT_INFO=%22MS4wLjABAAAALY8T0J9Cvs1Ra7VqRsuEfbXxR5ABPzgpdL0g_YiOddY%2F1673193600000%2F0%2F1673167259541%2F0%22; msToken=tIJtC-kCsqJtrNmrt-I05BVX2g5Ifhd3zqqaQ9lCQHzXpqIiB8KaJQhlT8Fk3F4HjZisNjqc04S73lW6CAsU-RD7U5fDq58Q0-pIVXaYe8X7yKcd_MQXrbIGmIL0Jg==; tt_scid=gx5QA1Gx8WBJxAWkT9PmHiQB-141-Lw5jR3eYc4y9KVSWXB5WpE9KLQOgheEZs.ifac0; msToken=TQGYYmG9jRzO1R_8gFTaaEJ30de9RhYAvowbXJi2U7qKGdf2ELRBLfra3CIbuHWTpqJIhf-huPDj7o3z4d8Zi5pXX2r1_PFipTM2_9L6-Z3JQQnxXRDrniyLGQJOSQ==; passport_fe_beating_status=true",
            "referer": "https://www.douyin.com/search/%E5%A5%88%E9%9B%AA?aid=76dfeef6-3fd1-4071-afe8-113ebcf170fa&publish_time=0&sort_type=0&source=normal_search&type=general",
            "sec-ch-ua": '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        return _headers

    def write_record(self, data: dict):
        # Write File
        f = open(f"{self.video_file_name}.csv", "a+")
        csv_obj = csv.writer(f)
        csv_obj.writerow(
            [
                data["author_nickname"], data["author_dyid"], data["aweme_id"],
                data["create_time"], data["desc"], data["share_url"],
                data["comment_count"], data["like_count"], data["share_count"],
            ]
        )
        f.close()

    def write_comment(self, c_list: list):
        f = open(f"{self.comment_file_name}.csv", "a+")
        csv_obj = csv.writer(f)
        for i in c_list:
            csv_obj.writerow(
                [
                    i["aweme_id"], i["like_count"],
                    i["remark_count"], i["content"],
                ]
            )
        f.close()

    def handle_video(self, data: dict):
        res = {
            # 博主信息
            "author_nickname": data["aweme_info"]["author"]["nickname"],
            "author_dyid": data["aweme_info"]["author"]["short_id"],

            # 视频信息
            "aweme_id": data["aweme_info"]["aweme_id"],
            "create_time": data["aweme_info"]["create_time"],
            "desc": data["aweme_info"]["desc"],
            "share_url": data["aweme_info"]["share_info"]["share_url"],
            "comment_count": data["aweme_info"]["statistics"]["comment_count"],
            "like_count": data["aweme_info"]["statistics"]["digg_count"],
            "share_count": data["aweme_info"]["statistics"]["share_count"],
        }
        self.write_record(res)
        try:
            self.handle_comment(res["aweme_id"], offset=0)
        except Exception:
            logger.exception("handle_video error")

    def handle_comment(self, aweme_id: str = None, comment_id: str = None, offset: int = None):
        while True:
            _comments = self.list_comment(aweme_id,
                                          comment_id=comment_id,
                                          offset=offset)
            comments = _comments["comments"]
            c_list = []
            for i in comments:
                c_list.append(
                    {
                        "aweme_id": aweme_id,
                        "content": i["text"],
                        "like_count": i["digg_count"],
                        "remark_count": i.get("reply_comment_total", 0),
                    }
                )
                if i.get("reply_comment_total"):
                    self.handle_comment(aweme_id, comment_id=i["cid"], offset=0)

            self.write_comment(c_list)
            if not _comments.get("has_more"):
                break


obj = Main()
obj.start()
