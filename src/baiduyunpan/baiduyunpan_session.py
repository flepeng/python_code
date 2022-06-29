# -*- coding:utf-8 -*-
"""
    @Time  : 2021/12/7  19:48
    @Author: Feng Lepeng
    @File  : baidupan.py
    @Desc  :
"""
import requests
import re
import json
import time
import random
# 解决验证码问题，经过测试实际使用过程中不会出验证码，所以没装的话可以屏蔽掉
# import pytesseract
from PIL import Image
from io import BytesIO

"""
初次使用时，请先从浏览器的开发者工具中获取百度网盘的Cookie，并设置在init方法中进行配置，并调用verifyCookie方法测试Cookie的有效性
已实现的方法：
1.获取登录Cookie有效性；
2.获取网盘中指定目录的文件列表；
3.获取加密分享链接的提取码；
4.转存分享的资源；
5.重命名网盘中指定的文件；
6.删除网盘中的指定文件；
7.移动网盘中指定文件至指定目录；
8.创建分享链接；
"""


class BaiDuPan(object):
    
    def __init__(self):
        # 创建session并设置初始登录Cookie
        self.session = requests.session()
        self.session.cookies['BDUSS'] = '0wzTmRKNkJQeE40OE1iNGZWOTBXTzNWbWdOb1VDWS0yWnlFZWFvZWRUb35odEpoRVFBQUFBJCQAAAAAAAAAAAEAAAD0jRhHMXBlcnBsZTFjaXR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD~5qmE~-apha'
        self.session.cookies['STOKEN'] = 'ba71ad462dcdcc7e572ba7b5e56013686451a971fb0fe9fb549b254738cd5d0a'
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
            # 'Cookie': 'XFCS=5418BC65472A2580F916651C1A558FD5A140D2E3FDD76EA6E4426B7D9766AFB5; XFT=8fKBUh5gMCrrIu9ykzevlrH4bkwAGmFDjzIHVAzc8zc=; __yjs_duid=1_08395eeac00d5291fd09a73a27e4044f1618560903745; PSTM=1618561872; BIDUPSID=81E5E1A1359DB4A0B2412DB3B8690E85; secu=1; PANWEB=1; MCITY=-:; BAIDUID=CF737B9E18D399CFC5B34668F5476D71:FG=1; csrfToken=n1K57BiuzdwDRdG7iTRAOqbo; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1638341114,1638594047,1638594134,1638594854; BDCLND=w9qgWD5TjpUceg/8ROvjRZsQr5MwOHqHluBS3iZHn4Q=; BDUSS=0wzTmRKNkJQeE40OE1iNGZWOTBXTzNWbWdOb1VDWS0yWnlFZWFvZWRUb35odEpoRVFBQUFBJCQAAAAAAAAAAAEAAAD0jRhHMXBlcnBsZTFjaXR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD~5qmE~-apha; BDUSS_BFESS=0wzTmRKNkJQeE40OE1iNGZWOTBXTzNWbWdOb1VDWS0yWnlFZWFvZWRUb35odEpoRVFBQUFBJCQAAAAAAAAAAAEAAAD0jRhHMXBlcnBsZTFjaXR5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD~5qmE~-apha; STOKEN=ba71ad462dcdcc7e572ba7b5e56013686451a971fb0fe9fb549b254738cd5d0a; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1638594901; ndut_fmt=3A721DDDEE1FF928EA84F2242919D05B210425B58337295F10EF327742A7E946; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDSFRCVID=SxkOJexroG04tO3HGNA5bfRzK9NbUdrTDYrEQ-mAp1wm6V8VJeC6EG0Pts1-dEu-EHtdogKK0mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tJ4q_IPMJK_3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDkCLxQcy4LdjG5C0Pb7WIQ75KQttpvboMOlj47mXpKw3-Aq54RX5D6rbhchMxbnohcLXPQhQfbQ0M6uqP-jW5TaaJ6D-n7JOpkxhfnxyb5bQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IeJRCH_ItKJDvKeJbYK4oj5KCyMfca5C6JKCOa3RA8Kb7Vbn7F5fnkbfJBD4QQWpRiLmbmWR7JW-3iVPjzyT3PDnK7yajK2M-8Km7f0n5C3RoDDKKmXUJpQT8rM-FOK5OibmjgLl7Oab3vOIJzXpO156kzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqjttJbKfoI82f-5_jJ7kqtbSMttfqx6betJyaR3C0fJvWJ5TMC_mLp3AhRDnLNOCBxnfyN7DXnTOyl38ShPCb6bIQPCBeqQqapJvJ6bE_hkX3l02Vbnae-t2ynLIy-rTBtRMW20jWl7mWPLWsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjC5j55-eH-ft5nB--ob04OV5bu3qCJqXU6qLT5XLpb4WM_tWgADKJncbMn6qqjzKn3xyl0njxQy5hbutektXp5tblcWqIO50MonDh8J3H7MJUntBGFLWtTO5hvvhb6O3M7-eMKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQbG_EJ6njKC_X3JjV5PK_Hn7zepbWMU4pbq7H2M-jJTn9ohnTBqDhHRQ-2x4BX4DAbh5n0pcH3GCLWljMt43VMxL93x6qLTKkQN3T-ntDHCn4L66NWPbfDn3oyT3VXp0nj4Rly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KCbtCthhx5; BDSFRCVID_BFESS=SxkOJexroG04tO3HGNA5bfRzK9NbUdrTDYrEQ-mAp1wm6V8VJeC6EG0Pts1-dEu-EHtdogKK0mOTH6KF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tJ4q_IPMJK_3qR5gMJ5q-n3HKUrL5t_XbI6y3JjOHJOoDDkCLxQcy4LdjG5C0Pb7WIQ75KQttpvboMOlj47mXpKw3-Aq54RX5D6rbhchMxbnohcLXPQhQfbQ0M6uqP-jW5TaaJ6D-n7JOpkxhfnxyb5bQRPH-Rv92DQMVU52QqcqEIQHQT3m5-5bbN3ut6IeJRCH_ItKJDvKeJbYK4oj5KCyMfca5C6JKCOa3RA8Kb7Vbn7F5fnkbfJBD4QQWpRiLmbmWR7JW-3iVPjzyT3PDnK7yajK2M-8Km7f0n5C3RoDDKKmXUJpQT8rM-FOK5OibmjgLl7Oab3vOIJzXpO156kzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksDMDtqjttJbKfoI82f-5_jJ7kqtbSMttfqx6betJyaR3C0fJvWJ5TMC_mLp3AhRDnLNOCBxnfyN7DXnTOyl38ShPCb6bIQPCBeqQqapJvJ6bE_hkX3l02Vbnae-t2ynLIy-rTBtRMW20jWl7mWPLWsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjC5j55-eH-ft5nB--ob04OV5bu3qCJqXU6qLT5XLpb4WM_tWgADKJncbMn6qqjzKn3xyl0njxQy5hbutektXp5tblcWqIO50MonDh8J3H7MJUntBGFLWtTO5hvvhb6O3M7-eMKmDloOW-TB5bbPLUQF5l8-sq0x0bOte-bQbG_EJ6njKC_X3JjV5PK_Hn7zepbWMU4pbq7H2M-jJTn9ohnTBqDhHRQ-2x4BX4DAbh5n0pcH3GCLWljMt43VMxL93x6qLTKkQN3T-ntDHCn4L66NWPbfDn3oyT3VXp0nj4Rly5jtMgOBBJ0yQ4b4OR5JjxonDh83bG7MJUutfD7H3KCbtCthhx5; H_PS_PSSID=35360_35104_31254_35237_34584_34518_35233_34579_35168_35328_35319_26350_35301; delPer=0; PSINO=1; BAIDUID_BFESS=CF737B9E18D399CFC5B34668F5476D71:FG=1',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        self.get_bdstoken()

    def get_bdstoken(self):
        response = self.session.get('https://pan.baidu.com/disk/home?', headers=self.headers)
        self.bdstoken = re.findall(r'"bdstoken":".*?"', response.content.decode("utf-8"))[0]
        print(self.bdstoken)

    def verifyCookie(self):
        """
        验证Cookie是否已登录，返回值errno代表的意思：
        0 有效的Cookie；1 init方法中未配置登录Cookie；2 无效的Cookie
        """
        if (self.session.cookies['BDUSS'] == '' or self.session.cookies['STOKEN'] == ''):
            return {'errno': 1, 'err_msg': '请在init方法中配置百度网盘登录Cookie'}
        else:
            response = self.session.get('https://pan.baidu.com/', headers=self.headers)
            home_page = response.content.decode("utf-8")
            if ('<title>百度网盘-全部文件</title>' in home_page):
                user_name = re.findall(r'username\":\"(.+?)\"', home_page)[0]
                # user_name = re.findall(r'\, \'(.+?)\'\)', home_page)[0]
                return {'errno': 0, 'err_msg': '有效的Cookie，用户名：%s' % user_name}
            else:
                return {'errno': 2, 'err_msg': '无效的Cookie！'}

    """
    获取指定目录的文件列表，直接返回原始的json
    """
    def getFileList(self, dir='/', order='time', desc=0, page=1, num=100):
        """
        构造获取文件列表的URL：
        https://pan.baidu.com/api/list?
        bdstoken=  从首页中可以获取到
        &dir=/  需要获取的目录
        &order=name  可能值：name，time，size
        &desc=0  0表示正序，1表示倒序
        &page=  第几页
        &num=100  每页文件数量
        &t=0.8685513844705777  推测为随机字符串
        &startLogTime=1581862647373  时间戳
        &logid=MTU4MTg2MjY0NzM3MzAuMzM2MTAzMzk5MTg3NzYyOQ==  固定值
        &clienttype=0  固定值
        &showempty=0  固定值
        &web=1  固定值
        &channel=chunlei  固定值
        &app_id=250528  固定值
        """
        # 访问首页获取bdstoken 

        t = random.random()
        startLogTime = str(int(time.time()) * 1000)
        url = 'https://pan.baidu.com/api/list?bdstoken=%s&dir=%s&order=%s&desc=%s&page=%s&num=%s&t=%s&startLogTime=%s\
                &logid=MTU4MTg2MjY0NzM3MzAuMzM2MTAzMzk5MTg3NzYyOQ==&clienttype=0&showempty=0&web=1&channel=chunlei&app_id=250528' \
              % (self.bdstoken, dir, order, desc, page, num, t, startLogTime)
        headers = self.headers
        headers['Referer'] = 'https://pan.baidu.com/disk/home?'
        response = self.session.get(url, headers=headers)
        print(response.json())
        return response.json()

    """
    获取分享链接的提取码
    返回值errno代表的意思：
    0 提取码获取成功；1 提取码获取失败；
    """
    @staticmethod
    def getSharePwd(surl):
        # 云盘精灵的接口
        ypsuperkey_headers = {
            'Host': 'ypsuperkey.meek.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        response = requests.get('https://ypsuperkey.meek.com.cn/api/v1/items/BDY-%s?client_version=2019.2' % surl,
                                headers=ypsuperkey_headers)
        pwd = response.json().get('access_code', '')
        if (not pwd):
            # 小鸟云盘搜索接口
            aisou_headers = {
                'Host': 'helper.aisouziyuan.com',
                'Origin': 'https://pan.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                'Referer': 'https://pan.baidu.com/share/init?surl=%s' % surl,
            }
            form_data = {
                'url': surl,
                'wrong': 'false',
                'type': 'baidu',
                'v': '3.132',
            }
            response = requests.post('https://helper.aisouziyuan.com/Extensions/Api/ResourcesCode?v=3.132',
                                     headers=aisou_headers, data=form_data)
            pwd = response.text
        errno, err_msg = (0, '提取码获取成功') if pwd else (1, '提取码获取失败：%s' % response.text)
        return {'errno': errno, 'err_msg': err_msg, 'pwd': pwd}

    """
    识别 验证加密分享时的验证码
    返回值errno代表的意思：
    0 识别成功；1 识别失败；其他值 获取验证码失败；
    """
    def vcodeOCR(self):
        # 获取验证码
        vcode_res = requests.get(
            'https://pan.baidu.com/api/getcaptcha?prod=shareverify&web=1&channel=chunlei&web=1&app_id=250528&bdstoken=null&clienttype=0',
            headers=self.headers)
        vcode_json = vcode_res.json()
        if (vcode_json['errno'] == 0):
            # 获取验证码图片
            genimage = requests.get(vcode_json['vcode_img'], headers=self.headers)
            # 非自动化脚本，可以改为人工识别，并且将人工识别的验证码保存，用于后续的CNN训练
            vcode_image = BytesIO(genimage.content)
            image = Image.open(vcode_image)
            image.show()
            vcode = input('请输入验证码：')
            f = open('./vcodeImg/%s - %s.jpg' % (vcode, str(int(time.time()) * 1000)), 'wb')
            f.write(genimage.content)
            f.close()

            """
            将验证码图片加载至内存中进行自动识别
            由于验证码旋转和紧贴，所以导致pytesseract识别率非常底！
            考虑基于CNN深度学习识别，筹备数据集需要一定的时间
            临时解决方案是：识别失败进行重试，加大重试次数
            """
            # vcode_image = BytesIO(genimage.content)
            # image = Image.open(vcode_image)                
            # vcode = pytesseract.image_to_string(image)
            errno, err_msg = (1, '识别失败') if (len(vcode) != 4) else (0, '识别成功')
            vcode_str = vcode_json['vcode_str']
        else:
            errno = vcode_json['errno']
            err_msg = '获取验证码失败'
            vcode_str = ''
        return {'errno': errno, 'err_msg': err_msg, 'vcode': vcode, 'vcode_str': vcode_str}

    """
    验证加密分享
    返回值errno代表的意思：
    0 加密分享验证通过；1 验证码获取失败；2 提取码不正确；3 加密分享验证失败；4 重试几次后，验证码依旧不正确；
    """
    def verifyShare(self, surl, bdstoken, pwd, referer):
        """
        构造密码验证的URL：https://pan.baidu.com/share/verify?
        surl=62yUYonIFdKGdAaueOkyaQ  从重定向后的URL中获取
        &t=1572356417593  时间戳
        &channel=chunlei  固定值
        &web=1  固定值
        &app_id=250528  固定值
        &bdstoken=742aa0d6886423a5503bbc67afdb2a7d  从重定向后的页面中可以找到，有时候会为空，经过验证，不要此字段也可以
        &logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==  不知道什么作用，暂时为空或者固定值都可以
        &clienttype=0  固定值
        """
        t = str(int(time.time()) * 1000)
        url = 'https://pan.baidu.com/share/verify?surl=%s&t=%s&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
                &logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==&clienttype=0' % (surl, t, bdstoken)
        form_data = {
            'pwd': pwd,
            'vcode': '',
            'vcode_str': '',
        }
        # 设置重试机制
        is_vcode = False
        for n in range(1, 166):
            # 自动获取并识别验证码，使用pytesseract自动识别时，可加大重试次数
            if is_vcode:
                ocr_result = self.vcodeOCR()
                if (ocr_result['errno'] == 0):
                    form_data['vcode'] = ocr_result['vcode']
                    form_data['vcode_str'] = ocr_result['vcode_str']
                elif (ocr_result['errno'] == 1):
                    continue
                else:
                    return {'errno': 1, 'err_msg': '验证码获取失败：%d' % ocr_result['errno']}
            headers = self.headers
            headers['referer'] = referer
            # verify_json['errno']：-9表示提取码不正确；-62表示需要验证码/验证码不正确（不输入验证码也是此返回值）
            verify_res = self.session.post(url, headers=headers, data=form_data)
            verify_json = verify_res.json()
            if (verify_json['errno'] == 0):
                return {'errno': 0, 'err_msg': '加密分享验证通过'}
            elif (verify_json['errno'] == -9):
                return {'errno': 2, 'err_msg': '提取码不正确'}
            elif (verify_json['errno'] == -62):
                is_vcode = True
            else:
                return {'errno': 3, 'err_msg': '加密分享验证失败：%d' % verify_json['errno']}
        return {'errno': 4,
                'err_msg': '重试多次后，验证码依旧不正确：%d' % (verify_json['errno'] if ("verify_json" in locals()) else -1)}

    """
    返回值errno代表的意思：
    0 转存成功；1 无效的分享链接；2 分享文件已被删除；
    3 分享文件已被取消；4 分享内容侵权，无法访问；5 找不到文件；6 分享文件已过期
    7 获取提取码失败；8 获取加密cookie失败； 9 转存失败；
    """
    def saveShare(self, url, pwd=None, path='/'):
        share_res = self.session.get(url, headers=self.headers)
        share_page = share_res.content.decode("utf-8")
        """
        1.如果分享链接有密码，会被重定向至输入密码的页面；
        2.如果分享链接不存在，会被重定向至404页面https://pan.baidu.com/error/404.html，但是状态码是200；
        3.如果分享链接已被删除，页面会提示：啊哦，你来晚了，分享的文件已经被删除了，下次要早点哟。
        4.如果分享链接已被取消，页面会提示：啊哦，你来晚了，分享的文件已经被取消了，下次要早点哟。
        5.如果分享链接涉及侵权，页面会提示：此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！
        6.啊哦！链接错误没找到文件，请打开正确的分享链接!
        7.啊哦，来晚了，该分享文件已过期
        """
        if ('error/404.html' in share_res.url):
            return {"errno": 1, "err_msg": "无效的分享链接", "extra": "", "info": ""}
        if ('你来晚了，分享的文件已经被删除了，下次要早点哟' in share_page):
            return {"errno": 2, "err_msg": "分享文件已被删除", "extra": "", "info": ""}
        if ('你来晚了，分享的文件已经被取消了，下次要早点哟' in share_page):
            return {"errno": 3, "err_msg": "分享文件已被取消", "extra": "", "info": ""}
        if ('此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问' in share_page):
            return {"errno": 4, "err_msg": "分享内容侵权，无法访问", "extra": "", "info": ""}
        if ('链接错误没找到文件，请打开正确的分享链接' in share_page):
            return {"errno": 5, "err_msg": "链接错误没找到文件", "extra": "", "info": ""}
        if ('啊哦，来晚了，该分享文件已过期' in share_page):
            return {"errno": 6, "err_msg": "分享文件已过期", "extra": "", "info": ""}

        # 提取码校验的请求中有此参数
        bdstoken = re.findall(r'bdstoken\":\"(.+?)\"', share_page)
        bdstoken = bdstoken[0] if (bdstoken) else ''
        # 如果加密分享，需要验证提取码，带上验证通过的Cookie再请求分享链接，即可获取分享文件
        if ('init' in share_res.url):
            surl = re.findall(r'surl=(.+?)$', share_res.url)[0]
            if (pwd == None):
                pwd_result = self.getSharePwd(surl)
                if (pwd_result['errno'] != 0):
                    return {"errno": 7, "err_msg": pwd_result['err_msg'], "extra": "", "info": ""}
                else:
                    pwd = pwd_result['pwd']
            referer = share_res.url
            verify_result = self.verifyShare(surl, bdstoken, pwd, referer)
            if (verify_result['errno'] != 0):
                return {"errno": 8, "err_msg": verify_result['err_msg'], "extra": "", "info": ""}
            else:
                # 加密分享验证通过后，使用全局session刷新页面（全局session中带有解密的Cookie）
                share_res = self.session.get(url, headers=self.headers)
                share_page = share_res.content.decode("utf-8")
        # 更新bdstoken，有时候会出现 AttributeError: 'NoneType' object has no attribute 'group'，重试几次就好了
        share_data = json.loads(re.search("yunData.setData\(({.*})\)", share_page).group(1))
        bdstoken = share_data['bdstoken']
        shareid = share_data['shareid']
        _from = share_data['uk']
        """
        构造转存的URL，除了logid不知道有什么用，但是经过验证，固定值没问题，其他变化的值均可在验证通过的页面获取到
        """
        save_url = 'https://pan.baidu.com/share/transfer?shareid=%s&from=%s&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
                    &logid=MTU3MjM1NjQzMzgyMTAuMjUwNzU2MTY4MTc0NzQ0MQ==&clienttype=0' % (shareid, _from, bdstoken)
        file_list = share_data['file_list']['list']
        form_data = {
            # 这个参数一定要注意，不能使用['fs_id', 'fs_id']，谨记！
            'fsidlist': '[' + ','.join([str(item['fs_id']) for item in file_list]) + ']',
            'path': path,
        }
        headers = self.headers
        headers['Origin'] = 'https://pan.baidu.com'
        headers['referer'] = url
        """
        用带登录Cookie的全局session请求转存
        如果有同名文件，保存的时候会自动重命名：类似xxx(1)
        暂时不支持超过文件数量的文件保存
        """
        save_res = self.session.post(save_url, headers=headers, data=form_data)
        save_json = save_res.json()
        errno, err_msg, extra, info = (0, '转存成功', save_json['extra'], save_json['info']) if (
                save_json['errno'] == 0) else (9, '转存失败：%d' % save_json['errno'], '', '')
        return {'errno': errno, 'err_msg': err_msg, "extra": extra, "info": info}

    """
    重命名指定文件
    0 重命名成功；1 重命名失败；
    """
    def rename(self, path, newname):
        """
        构造重命名的URL：https://pan.baidu.com/api/filemanager?
        bdstoken=  从首页可以获取到
        &opera=rename  固定值
        &async=2  固定值
        &onnest=fail  固定值
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        """
        url = 'https://pan.baidu.com/api/filemanager?bdstoken=%s&opera=rename&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528\
                &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        form_data = {"filelist": "[{\"path\":\"%s\",\"newname\":\"%s\"}]" % (path, newname)}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '重命名成功！'}
        else:
            return {'errno': 1, 'err_msg': '重命名失败！', 'info': response.json()}

    """
    删除指定文件
    0 删除成功；1 删除失败；
    """
    def delete(self, path):
        """
        构造重命名的URL：https://pan.baidu.com/api/filemanager?
        bdstoken=  从首页可以获取到
        &opera=delete  固定值
        &async=2  固定值
        &onnest=fail  固定值
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        """
        url = 'https://pan.baidu.com/api/filemanager?bdstoken=%s&opera=delete&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528\
                &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        form_data = {"filelist": "[\"%s\"]" % path}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '删除成功！'}
        else:
            return {'errno': 1, 'err_msg': '删除失败！', 'info': response.json()}

    """
    移动文件至指定目录
    0 删除成功；1 删除失败；
    """
    def move(self, path, destination, newname=False):
        """
        构造重命名的URL：https://pan.baidu.com/api/filemanager?
        bdstoken=  从首页可以获取到
        &opera=move  固定值
        &async=2  固定值
        &onnest=fail  固定值
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        """
        url = 'https://pan.baidu.com/api/filemanager?bdstoken=%s&opera=move&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528\
                &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        if (not newname):
            newname = path.split('/')[-1]
        form_data = {
            "filelist": "[{\"path\":\"%s\",\"dest\":\"%s\",\"newname\":\"%s\"}]" % (path, destination, newname)}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '移动成功！'}
        else:
            return {'errno': 1, 'err_msg': '移动失败！', 'info': response.json()}

    """
    随机生成4位字符串
    """
    @staticmethod
    def generatePwd(n=4):
        pwd = ""
        for i in range(n):
            temp = random.randrange(0, 3)
            if temp == 0:
                ch = chr(random.randrange(ord('A'), ord('Z') + 1))
                pwd += ch
            elif temp == 1:
                ch = chr(random.randrange(ord('a'), ord('z') + 1))
                pwd += ch
            else:
                pwd = str((random.randrange(0, 10)))
        return pwd

    """
    创建分享链接
    fid_list为列表，例如：[1110768251780445]
    0 创建成功；1 创建失败；
    """
    def createShareLink(self, fid_list, period=0, pwd=False):
        """
        构造重命名的URL：https://pan.baidu.com/share/set?
        bdstoken=  从首页可以获取到
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        """
        url = 'https://pan.baidu.com/share/set?bdstoken=%s&channel=chunlei&web=1&app_id=250528\
                &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        if (not pwd):
            pwd = self.generatePwd()

        """
        schannel=4  不知道什么意思，固定为4
        channel_list=[]  不知道什么意思，固定为[]
        period=0  0表示永久，7表示7天
        pwd=w4y5  分享链接的提取码，可自定义
        fid_list=[1110768251780445]  分享文件的id列表，可调用getFileList方法获取文件列表，包含fs_id
        """
        form_data = {
            'schannel': 4,
            'channel_list': '[]',
            'period': period,
            'pwd': pwd,
            'fid_list': str(fid_list),
        }
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '创建分享链接成功！', 'info': {'link': response.json()['link'], 'pwd': pwd}}
        else:
            return {'errno': 1, 'err_msg': '创建分享链接失败！', 'info': response.json()}


if __name__ == '__main__':
    obj = BaiDuPan()
    print(obj.verifyCookie())
    obj.getFileList('/书籍')
    print(obj.createShareLink('[165681573819616]'))

