# -*- coding:utf-8 -*-
"""
    @Time  : 2021/12/7  17:48
    @Author: Feng Lepeng
    @File  :
    @Desc  :
        - 百度网盘开放平台地址：https://pan.baidu.com/union/doc/
        - 参考git
            - https://github.com/iyzyi/BaiduYunTransfer
            - https://github.com/hxz393/BaiduPanFilesTransfers
            - https://github.com/Jljqbd/baidupan/blob/b5f24cd238a807f7f0e2095e6ac03f7fa7a26a90/BaiduPan.py
"""
import re
import os
import time
import json
import requests
import urllib
import datetime
import hashlib
import webbrowser
import configparser
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Referer': 'pan.baidu.com'
}

universal_error_code = {
    '2': '参数错误。检查必填字段；get/post 参数位置',
    '-6': '身份验证失败。access_token 是否有效；部分接口需要申请对应的网盘权限',
    '31034': '命中接口频控。核对频控规则;稍后再试;申请单独频控规则',
    '42000': '访问过于频繁',
    '42001': 'rand校验失败',
    '42999': '功能下线',
    '9100': '一级封禁',
    '9200': '二级封禁',
    '9300': '三级封禁',
    '9400': '四级封禁',
    '9500': '五级封禁'
}


class OPConfig(object):
    """
    ini配置文件是被configParser直接解析然后再加载的，如果只是修改配置文件，并不会改变已经加载的配置
    同时也说明 配置文件只会被加载一次
    """

    _instance_lock = threading.Lock()

    def __init__(self, file_name='config.ini'):
        # file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__name__))), file_name)
        self.file_name = file_name
        self.config = configparser.ConfigParser()
        self.config.read(file_name)

    def __new__(cls, *arg, **kwargs):
        """
        single mode，the config file must be control by the only one
        :param arg:
        :param kwargs:
        :return:
        """
        if not hasattr(OPConfig, "_instance"):
            with OPConfig._instance_lock:
                if not hasattr(OPConfig, "_instance"):
                    OPConfig._instance = object.__new__(cls)
        return OPConfig._instance

    def get_config(self, section, k):
        return self.config.get(section, k)

    def get_section(self):
        return self.config.sections()

    def get_section_all_key(self, section):
        return self.config.options(section)

    def add_section(self, section):
        self.config.add_section(section)

    def update_k(self, section, k, v):
        """
        更新相应的k，如果没有对应的k，会自动创建 k，判断k时不区分大小写。
        :param section:
        :param k:
        :param v:
        :return:
        """
        self.config.set(section, k, v)

    def remove_section(self, section):
        self.config.remove_section(section)

    def remove_k(self, section, k):
        self.config.remove_option(section, k)

    def save_config(self):
        with open(self.file_name, "w+") as f:
            self.config.write(f)


class BaiduYunInit:
    """
    百度云 初始化 类
    """

    def __init__(self):
        """
        按照https://pan.baidu.com/union/document/entrance#%E7%AE%80%E4%BB%8B 的指引，申请api_key和secret_key。
        出于安全和QPS的考量，推荐申请自己的api_key和secret_key。
        """
        self.opc = OPConfig()
        self.api_key = self.opc.get_config("Default", "Appkey")
        self.secret_key = self.opc.get_config("Default", "Secretkey")
        self.access_token = ''
        self.refresh_token = ''
        self.headers = headers

    def apply_for_token(self):
        """
        获取应用授权的流程：先获取授权码code，再通过code得到token(access_token和refresh_token)
        详情参见：https://pan.baidu.com/union/document/entrance#3%E8%8E%B7%E5%8F%96%E6%8E%88%E6%9D%83
        :return:
        """
        """
        第一步：获取code
        参数：
            response_type       固定值，值为'code'
            client_id           自己应用的API key
            redirect_uri        授权回调地址。对于无server的应用，可将其值设为'oob'，回调后会返回一个平台提供默认回调地址
            scope               访问权限，即用户的实际授权列表，值为'basic', 'netdisk'二选一，含义分别为基础权限（访问您的个人资料等基础信息），百度网盘访问权限（在您的百度网盘创建文件夹并读写数据）
            display             授权页的展示方式，默认为'page'
        """
        get_code_url = 'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={}&redirect_uri=oob&scope=netdisk'.format(
            self.api_key)
        code = input('请访问下面的链接：\n%s\n登录百度账号，并将授权码粘贴至此处，然后回车，完成授权：\n' % get_code_url)

        """
        第二步：通过code，获取token
        参数：
            grant_type          固定值，值为'authorization_code'
            code                上一步得到的授权码
            client_id           应用的API KEY
            client_secret       应用的SECRET KEY
            redirect_uri        和上一步的redirect_uri相同
        """
        try:
            get_token_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code'
            params = {'code': code, 'client_id': self.api_key, 'client_secret': self.secret_key, 'redirect_uri': 'oob'}
            res = requests.get(get_token_url, headers=self.headers, params=params)
            res_json = res.json()
        except Exception as e:
            print('请检查网络是否连通：%s' % e)
            return False

        if 'error' in res_json:
            error = res_json['error']
            print('获取token失败：%s' % error)
            return False
        elif 'access_token' in res_json and 'refresh_token' in res_json:
            self.access_token = res_json['access_token']
            self.refresh_token = res_json['refresh_token']
            return True

    def reflush_token(self):
        """
        使用 refresh_token，刷新token。
        """
        try:
            reflush_token_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token'
            params = {'refresh_token': self.refresh_token, 'client_id': self.api_key, 'client_secret': self.secret_key}
            res = requests.get(reflush_token_url, headers=self.headers, params=params)
            res_json = res.json()
        except Exception as e:
            print('请检查网络是否连通：%s' % e)
            return False

        if 'error' in res_json:
            error = res_json['error']
            print('刷新token失败：%s' % error)
            return False
        elif 'access_token' in res_json and 'refresh_token' in res_json:
            self.access_token = res_json['access_token']
            self.refresh_token = res_json['refresh_token']
            return True

    def init_token(self):
        """
        access_token的有效期是一个月，refresh_token的有效期是十年，access_token过期后，使用refresh_token刷新token即可
        如果存在配置文件且token存在时间少于27天，则直接从配置文件中读入token
        如果存在配置文件且token存在时间大于27天，少于10个平年，则刷新token
        如果存在配置文件且token存在时间超过10个平年，则重新申请token
        如果不存在配置文件，则申请token
        """
        self.update_time = int(self.opc.get_config("Default", 'update_time'))
        self.access_token = self.opc.get_config("Default", 'access_token')
        self.refresh_token = self.opc.get_config("Default", 'refresh_token')
        now_time = int(time.time())

        # token存在时间少于27天，则直接从配置文件中读入token
        if self.access_token and self.refresh_token and now_time - self.update_time < 27 * 24 * 60 * 60:
            print('已从配置文件中读入token')

        # token存在时间大于27天，少于10个平年，则刷新token
        elif self.access_token and self.refresh_token and now_time - self.update_time < 10 * 315 * 24 * 60 * 60:
            self.reflush_token()
            self.opc.update_k("Default", 'access_token', self.access_token)
            self.opc.update_k("Default", 'refresh_token', self.refresh_token)
            self.opc.update_k("Default", 'update_time', str(now_time))
            self.opc.save_config()
            print('已刷新token并将token写入配置文件中')

        # 没有 获取到 token 或者 token存在时间超过10个平年，则重新申请token（10年后百度网盘还能不能用都不好说）
        else:
            self.apply_for_token()
            self.opc.update_k("Default", 'access_token', self.access_token)
            self.opc.update_k("Default", 'refresh_token', self.refresh_token)
            self.opc.update_k("Default", 'update_time', str(now_time))
            self.opc.save_config()
            print('已重新申请token并将token写入配置文件中')

        return True


class BaiduYunBase(BaiduYunInit):
    """
    百度云 基础操作 类
    """

    def get_user_info(self):
        """
        获取用户信息
        :return:
        """
        url = "https://pan.baidu.com/rest/2.0/xpan/nas?access_token=" + self.access_token + "&method=uinfo"
        headers = {
            'User-Agent': 'pan.baidu.com'
        }
        info = requests.get(url, headers=headers).json()
        self.login_status = info['errno'] == 0
        if self.login_status:
            vip = "超级会员" if info['vip_type'] == 2 else "普通用户"
            print(f"用户信息：{'-' * 10} {info['baidu_name']} - {info['netdisk_name']} - {vip} -{'-' * 10}")
            return info['baidu_name']
        else:
            print('登录失败！')

    def get_capacity(self):
        url = "https://pan.baidu.com/api/quota"
        get_data = requests.get(url, params={'access_token': self.access_token})
        data_json = json.loads(get_data.text)
        # 总空间大小，已使用大小
        print(f"总空间大小:{data_json['total']}，已使用大小:data_json['used'] ")
        return data_json['total'], data_json['used']

    def ls(self, dir='/'):
        """
        获取文件列表
        :param dir:
        :return:
        """
        files = 'https://pan.baidu.com/rest/2.0/xpan/file?method=list'
        get_data = requests.get(files,
                                params={'access_token': self.access_token, 'dir': dir, 'order': 'name', 'desc': '0'})
        data_json = json.loads(get_data.text)
        file_data = []
        for f in data_json['list']:
            element = {
                'path': f['path'],
                'fs_id': f['fs_id'],
                'isdir': f['isdir'],
                'size': f['size']
            }
            file_data.append(element)
        return file_data

    def upload(self, local_path):
        """
        上传文件，由于第三方上传应用的接口限制，上传的文件会存储在/apps/mypan_py/下
        文件上传分为三个阶段：预上传、分片上传、创建文件,先不支持分片上传，即大于4G的文件无法上传
        参考连接：https://pan.baidu.com/union/doc/3ksg0s9r7
        :param local_path: 要上传的文件本地路径
        :return:
        """
        upload_to_path = "/apps/" + local_path
        file_size = os.path.getsize(local_path)
        block_list = []
        with open(local_path, 'rb') as f:
            data = f.read()
            file_md5 = hashlib.md5(data).hexdigest()
            block_list.append(file_md5)
            f.close()
        block_list = json.dumps(block_list)

        # 第一步：预上传
        url_1 = "https://pan.baidu.com/rest/2.0/xpan/file?method=precreate"
        url_1 = url_1 + "&access_token=" + self.access_token
        payload = {
            'path': upload_to_path,
            'size': file_size,
            'rtype': '1',
            'isdir': '0',
            'autoinit': '1',
            'block_list': block_list
        }
        res_1 = requests.request("POST", url_1, data=payload)
        data_json = json.loads(res_1.text)
        print(data_json)
        uploadid = data_json['uploadid']

        # 第二步：分片上传
        url_2 = "https://d.pcs.baidu.com/rest/2.0/pcs/superfile2?method=upload"
        url_2 = url_2 + "&access_token=" + self.access_token + "&type=tmpfile&path=" + upload_to_path + "&uploadid=" + uploadid + "&partseq=0"
        files = [
            ('file', open(local_path, 'rb'))
        ]
        res_2 = requests.request("POST", url_2, files=files)
        data_json = json.loads(res_2.text)
        print(data_json)

        # 第三步：创建文件
        url_3 = "https://pan.baidu.com/rest/2.0/xpan/file?method=create"
        url_3 = url_3 + "&access_token=" + self.access_token
        payload = {
            'path': upload_to_path,
            'size': file_size,
            'rtype': '1',
            'isdir': '0',
            'uploadid': uploadid,
            'block_list': block_list
        }
        res_3 = requests.request("POST", url_3, data=payload)
        data_json = json.loads(res_3.text)
        print(data_json)
        return not data_json['errno']

    def download(self, filename, topath):
        # topath只要给出路径即可无需添加下载的文件的名称,且路径以‘/’结尾
        # filename为数组
        file_list = self.search(filename)
        download_url = []
        for f in filename:
            file_list = self.search(f)
            download_url.append(self.get_data([file_list[0]['fs_id']])[0]['dlink'])
        for index in range(len(download_url)):
            path = topath + filename[index]
            url = download_url[index] + "&access_token=" + self.access_token
            # urllib.request.urlretrieve(self.download_url[index] + "&access_token=" + self.access_token, download_path + self.filename[index])
            start = time.time()
            size = 0
            response = requests.get(url,
                                    stream=True)  # stream参数设置成True时，它不会立即开始下载，当你使用iter_content或iter_lines遍历内容或访问内容属性时才开始下载
            chunk_size = 1024  # 每次块大小为1024
            content_size = int(response.headers['content-length'])  # 返回的response的headers中获取文件大小信息
            print("文件大小：" + str(round(float(content_size / chunk_size / 1024), 4)) + "[MB]")
            with open(path, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):  # 每次只获取一个chunk_size大小
                    file.write(data)  # 每次只写入data大小
                    size = len(data) + size  # 'r'每次重新从开始输出，end = ""是不换行
                    print('\r' + "已经下载：" + int(size / content_size * 100) * "█" + " 【" + str(
                        round(size / chunk_size / 1024, 2)) + "MB】" + "【" + str(
                        round(float(size / content_size) * 100, 2)) + "%" + "】", end="")
            end = time.time()
            print("下载完成，总耗时:" + str(end - start) + "秒")

    def mydel(self, path):
        url = "https://pan.baidu.com/rest/2.0/xpan/file?method=filemanager"
        url = url + "&opera=delete&access_token=" + self.access_token
        payload = {
            'async': '1',
            'filelist': '["' + path + '"]',
            'ondup': 'fail'
        }
        res = requests.request("POST", url, data=payload)
        data_json = json.loads(res.text)
        return not data_json['errno']

    def search(self, key, path='/'):
        # key搜索的关键词，path搜索的路径
        url = "https://pan.baidu.com/rest/2.0/xpan/file?method=search"
        if path == "/":
            get_data = requests.get(url, params={'access_token': self.access_token, 'key': key, 'recursion': 1})
        else:
            get_data = requests.get(url,
                                    params={'access_token': self.access_token, 'key': key, 'recursion': 1, 'dir': path})
        data_json = json.loads(get_data.text)
        file_list_json = data_json['list']
        file_list = []
        for f in file_list_json:
            # fs_id, 路径， 大小（B）,是否是文件夹
            element = {
                'fs_id': f['fs_id'],
                'path': f['path'],
                'size': f['size'],
                'isdir': f['isdir']
            }
            file_list.append(element)
        return file_list

    def get_data(self, fsid):
        """
        查询文件信息:本接口用于获取用户指定文件的meta信息
        :param fsid:
        :return:
        """
        url = "https://pan.baidu.com/rest/2.0/xpan/multimedia?method=filemetas"
        fsid_str = ""
        fsid = fsid[0:99]
        for i in fsid:
            fsid_str = fsid_str + str(i) + ","
        fsid_str = fsid_str[0:-1]  # 最后一个多余的逗号去除
        url = url + '&access_token=' + self.access_token + f"&fsids=[{fsid_str}]&dlink=1"
        get_data = requests.get(url)
        data_json = json.loads(get_data.text)
        file_list_json = data_json['list']
        file_list = []
        for f in file_list_json:
            # fs_id, 路径， 大小（B）,是否是文件夹
            element = {
                'fs_id': f['fs_id'],
                'path': f['path'],
                'size': f['size'],
                'isdir': f['isdir'],
                'dlink': f['dlink']
            }
            file_list.append(element)
        return file_list

    def copy(self, oldpath, newpath):
        # 复制
        url = "https://pan.baidu.com/rest/2.0/xpan/file?method=filemanager"
        url = url + "&opera=copy&access_token=" + self.access_token
        d_l = newpath.split('/')
        dest = "/".join(d_l[0:-1])
        newname = d_l[-1]
        payload = {
            'async': '1',
            'filelist': '[{"path":"' + oldpath + '","dest":"' + dest + '","newname":"' + newname + '","ondup":"fail"}]',
            'ondup': 'fail'
        }
        res = requests.request("POST", url, data=payload)
        data_json = json.loads(res.text)
        return not data_json['errno']

    def move(self, oldpath, newpath):
        # 复制
        url = "https://pan.baidu.com/rest/2.0/xpan/file?method=filemanager"
        url = url + "&opera=move&access_token=" + self.access_token
        d_l = newpath.split('/')
        dest = "/".join(d_l[0:-1])
        newname = d_l[-1]
        payload = {
            'async': '2',
            'filelist': '[{"path":"' + oldpath + '","dest":"' + dest + '","newname":"' + newname + '","ondup":"fail"}]',
            'ondup': 'fail'
        }
        files = [
        ]
        res = requests.request("POST", url, data=payload, files=files)
        data_json = json.loads(res.text)
        return not data_json['errno']

    def rename(self, oldname, newname):
        # 注意调用时oldname包含绝对路径，newname只是新文件名称
        url = "https://pan.baidu.com/rest/2.0/xpan/file?method=filemanager"
        url = url + "&opera=rename&access_token=" + self.access_token
        d_1 = oldname.split('/')
        dest = '/'.join(d_1[0:-1])
        payload = {
            'async': 2,
            # 'filelist': ':[{path":"'+ oldname +'","newname":'+ newname +'"}]',
            'filelist': '[{"path":"' + oldname + '","dest":"' + dest + '","newname":"' + newname + '"}]',
            'ondup': 'fail'
        }
        res = requests.request("POST", url, data=payload)
        data_json = json.loads(res.text)
        return not data_json['errno']

    def create(self, path):
        url = 'https://pan.baidu.com/rest/2.0/xpan/file?method=create'
        url = url + '&access_token=' + self.access_token
        payload = {
            'path': path,
            'size': '0',
            'isdir': '1',
        }
        res_3 = requests.request("POST", url, data=payload)
        return not res_3['errno']


class BaiduYunTransfer(BaiduYunBase):
    """
    百度云 转存 类
    """

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def get_surl(self, share_link):
        """
        获取surl。举个例子：
        short_link: https://pan.baidu.com/s/1LGDt_UQfdyQ9ga04bsnLKg
        long_link: https://pan.baidu.com/share/init?surl=LGDt_UQfdyQ9ga04bsnLKg
        surl: LGDt_UQfdyQ9ga04bsnLKg
        """
        res = re.search(r'https://pan\.baidu\.com/share/init\?surl=([0-9a-zA-Z].+?)$', share_link)
        if res:
            print('long_link:', share_link)

            self.surl = res.group(1)
            print('surl:', self.surl)
            return True
        else:
            print('short_link:', share_link)

            res = requests.get(share_link, headers=self.headers)
            reditList = res.history
            if reditList == []:  # 当分享不存在时，不会输入验证码，而是直接显示链接不存在。
                print('链接不存在：此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！')
                return False
            link = reditList[len(reditList) - 1].headers["location"]  # 302跳转的最后一跳的url
            print('long_link:', link)

            res = re.search(r'/share/init\?surl=([0-9a-zA-Z].+$)', link)
            if res:
                self.surl = res.group(1)
                print('surl:', self.surl)
                return True
            else:
                print('获取surl失败')
                return False

    def get_sekey(self, password):
        """
        验证提取码是否正确，如果正确，得到一个与提取码有关的密钥串randsk(即后面获取文件目录信息和转存文件时需要用到的sekey)
        详情参见：https://pan.baidu.com/union/document/openLink#%E9%99%84%E4%BB%B6%E5%AF%86%E7%A0%81%E9%AA%8C%E8%AF%81
        """
        url = 'https://pan.baidu.com/rest/2.0/xpan/share?method=verify'
        params = {'surl': self.surl}
        data = {'pwd': password}
        res = requests.post(url, headers=self.headers, params=params, data=data)

        res_json = res.json()
        errno = res_json['errno']
        if errno == 0:
            randsk = res_json['randsk']
            self.sekey = urllib.parse.unquote(randsk, encoding='utf-8',
                                              errors='replace')  # 需要urldecode一下，不然%25会再次编码成%2525
            print('sekey:', self.sekey)
            return True
        else:
            error = {
                '105': '链接地址错误',
                '-12': '非会员用户达到转存文件数目上限',
                '-9': 'pwd错误',
                '2': '参数错误,或者判断是否有referer'}
            error.update(self.universal_error_code)

            # 提取码不是4位的时候，返回的errno是-12，含义是非会员用户达到转存文件数目上限，这是百度网盘的后端代码逻辑不正确，我也没办法。不过你闲的没事输入长度不是4位的提取码干嘛？
            if str(errno) in error:
                print('获取sekey失败，错误码：{}，错误：{}'.format(errno, error[str(errno)]))
            else:
                print(
                    '获取sekey失败，错误码：{}，错误未知，请尝试查询https://pan.baidu.com/union/document/error#%E9%94%99%E8%AF%AF%E7%A0%81%E5%88%97%E8%A1%A8'.format(
                        errno))

            return False

    def get_shareid_and_uk_and_fsidlist(self):
        """
        获取附件中的文件id列表，同时也会含有shareid和uk(userkey)
        详情参见：https://pan.baidu.com/union/document/openLink#%E8%8E%B7%E5%8F%96%E9%99%84%E4%BB%B6%E4%B8%AD%E7%9A%84%E6%96%87%E4%BB%B6%E5%88%97%E8%A1%A8
        shareid+uk和shorturl这两组参数只需要选择一组传入即可，这里我们不知道shareid和uk，所以传入shorturl，来获取文件列表信息和shareid和uk。
        参数：
        shareid             分享链接id
        uk                  分享用户id（userkey）
        shorturl            分享链接地址（就是前面提取出来的surl，如9PsW5sWFLdbR7eHZbnHelw，不是整个的绝对路径）
        page                数据量大时，需分页
        num                 每页个数，默认100
        root                为1时，表示显示链接根目录下所有文件
        fid                 文件夹ID，表示显示文件夹下的所有文件
        sekey               附件链接密钥串，对应verify接口返回的randsk
        """
        url = 'https://pan.baidu.com/rest/2.0/xpan/share?method=list'
        params = {"shorturl": self.surl, "page": "1", "num": "100", "root": "1", "fid": "0", "sekey": self.sekey}
        res = requests.get(url, headers=self.headers, params=params)
        res_json = res.json()

        res_json = res.json()
        errno = res_json['errno']
        if errno == 0:
            self.shareid = res_json['share_id']
            print('shareid:', self.shareid)

            self.uk = res_json['uk']
            print('uk:', self.uk)

            fsidlist = res_json['list']
            self.fsid_list = []
            for fs in fsidlist:
                self.fsid_list.append(int(fs['fs_id']))
            print('fsidlist:', self.fsid_list)

            return True
        else:
            error = {
                '110': '有其他转存任务在进行',
                '105': '非会员用户达到转存文件数目上限',
                '-7': '达到高级会员转存上限'
            }
            error.update(self.universal_error_code)

            if str(errno) in error:
                print('获取shareid, uk, fsidlist失败，错误码：{}，错误：{}'.format(errno, error[str(errno)]))
            else:
                print(
                    '获取shareid, uk, fsidlist失败，错误码：{}，错误未知，请尝试查询https://pan.baidu.com/union/document/error#%E9%94%99%E8%AF%AF%E7%A0%81%E5%88%97%E8%A1%A8'.format(
                        errno))

            return False

    def file_transfer(self, dir):
        """
        附件文件转存
        详情参见：https://pan.baidu.com/union/document/openLink#%E9%99%84%E4%BB%B6%E6%96%87%E4%BB%B6%E8%BD%AC%E5%AD%98
        不过上面链接中的参数信息好像有些不太对，里面的示例的用法是对的。
        GET参数：
        access_token        前面拿到的access_token
        shareid             分享链接id
        from                分享用户id（userkey）
        POST参数：
        sekey               附件链接密钥串，对应verify接口返回的randsk
        fsidlist            文件id列表，形如[557084550688759]，[557084550688759, 557084550688788]
        path                转存路径
        """
        url = 'http://pan.baidu.com/rest/2.0/xpan/share?method=transfer'
        params = {'access_token': self.access_token, 'shareid': self.shareid, 'from': self.uk, }
        data = {'sekey': self.sekey, 'fsidlist': str(self.fsid_list), 'path': dir}
        res = requests.post(url, headers=self.headers, params=params, data=data)

        res_json = res.json()
        errno = res_json['errno']
        if errno == 0:
            print('文件转存成功')
            return True
        else:
            error = {
                '111': '有其他转存任务在进行',
                '120': '非会员用户达到转存文件数目上限',
                '130': '达到高级会员转存上限',
                '-33': '达到转存文件数目上限',
                '12': '批量操作失败',
                '-3': '转存文件不存在',
                '-9': '密码错误',
                '5': '分享文件夹等禁止文件'}
            error.update(self.universal_error_code)

            if str(errno) in error:
                print('文件转存失败，错误码：{}，错误：{}\n返回JSON：{}'.format(errno, error[str(errno)], res_json))
            else:
                print(
                    '文件转存失败，错误码：{}，错误未知，请尝试查询https://pan.baidu.com/union/document/error#%E9%94%99%E8%AF%AF%E7%A0%81%E5%88%97%E8%A1%A8\n返回JSON：{}'.format(
                        errno, res_json))

            return False

        # 转存路径不存在时返回errno=2, 参数错误，如：{"errno":2,"request_id":5234720642281834903}
        # 自己转存自己分享的文件时返回errno=12，批量操作失败，如：{"errno":12,"task_id":0,"info":[{"path":"\/asm","errno":4,"fsid":95531336671296}]}
        # 转存成功后再次转存到同一文件夹下时返回errno=12，批量操作失败，如：{"errno":12,"task_id":0,"info":[{"path":"\/doax","errno":-30,"fsid":557084550688759}]}

    def transfer(self, share_link, password):
        if self.get_surl(share_link) and self.get_sekey(password) and self.get_shareid_and_uk_and_fsidlist():
            self.file_transfer()


def main():
    bdp = BaiduYunBase()
    if bdp.init_token():
        bdp.get_user_info()
        print(bdp.ls())
        bdp.upload("README.md")


if __name__ == '__main__':
    main()

    # share_link = 'https://pan.baidu.com/s/1E8WcGMjNp_t1hpCQ1COnAw'  # 分享链接
    # # share_link = 'https://pan.baidu.com/share/init?surl=9PsW5sWFLdbR7eHZbnHelw'    # 分享链接，以上两种形式的链接都可以
    # password = '1rmh'  # 分享提取码
    # dir = '/书籍'  # 转存路径，根路径为/
