# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/29  11:29
    @Author: Feng Lepeng
    @File  : manage_request.py
    @Desc  : 下载视频
"""
import os
import re
import sys
import time
import datetime
import requests
import logging
import pymysql
import threading
import configparser
from bs4 import BeautifulSoup
from queue import Queue

logger = logging.getLogger()

headers = {
    'referer': 'https://yiyi.55zuiday.com/share/wVuAcJFy1tMy4t0x',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

ffmpeg = "C:\\Users\\Administrator\\Downloads\\ffmpeg-2022-01-17-git-dcc9454ab9-essentials_build\\bin\\ffmpeg.exe"
zip = """C:\\"Program Files"\\WinRAR\\WinRAR.exe"""
cmd_ffmpeg = ffmpeg + """ -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -c copy "{}"
"""
cmd_ffmpeg_cut = ffmpeg + """ -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -ss 00:00:00.002 -c copy "{}"
"""

logger = logging.getLogger(__name__)


class MySQL(object):

    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            passwd=passwd,
            db=db,
            charset='utf8'
        )

    def select(self, sql, sql_parameter=None):
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql, sql_parameter)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            logger.exception('连接数据库出错')
            return []

    def exec_sql(self, sql):
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            return True
        except Exception as e:
            logger.exception('连接数据库出错')
            return False

    def update(self, sql):
        return self.exec_sql(sql)

    def insert(self, sql):
        return self.exec_sql(sql)

    def delete(self, sql):
        return self.exec_sql(sql)

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            logger.exception("关闭数据库失败")


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

    # single mode，the config file must be control by the only one
    def __new__(cls, *arg, **kwargs):
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
        # 更新相应的k，如果没有对应的k，会自动创建 k，判断k时不区分大小写。
        self.config.set(section, k, v)

    def remove_section(self, section):
        self.config.remove_section(section)

    def remove_k(self, section, k):
        self.config.remove_option(section, k)

    def save_config(self):
        with open(self.file_name, "w+") as f:
            self.config.write(f)


opc = OPConfig()
user = opc.get_config("MySQL_T", "user")
port = opc.get_config("MySQL_T", "port")
host = opc.get_config("MySQL_T", "host")
passwd = opc.get_config("MySQL_T", "passwd")
db = opc.get_config("MySQL_T", "db")
mysql = MySQL(host, port, user, passwd, db)


def zip_encrypt(old_file_name, new_file_name, passwd="Pass"):
    """
    zip and 加密
    :param old_file_name: 01_今日内容.mp4
    :param new_file_name: 01.rar
    :param passwd:
    :return:
    """
    cmd = zip + """ a -p{} "{}" "{}"
    """.format(passwd, new_file_name, old_file_name)
    os.system(cmd)


def save_url():
    url_base = opc.get_config("MySQL_T", "url_base")
    for i in range(1, 51):
        url = url_base.format(i)
        print(url)
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, features="lxml")
        tags = soup.find_all(attrs={"class": "is-one-quarter-desktop"})
        for tag in tags:
            video_url = tag.find("a").attrs.get("href")
            video_name = tag.find("p").text
            video_type = []
            for a in tag.find_all(attrs={"class": "theme-color"}):
                video_type.append(a.text)
            video_type = ",".join(video_type)
            sql = "insert into dstv(name, video_url, video_type) value('{}', '{}', '{}')".format(video_name, video_url,
                                                                                                 video_type)
            print(sql)
            mysql.insert(sql)
        time.sleep(2)


class Download_u3m8_ds():

    def get_m3u8_url(self, video_url):
        resp = requests.get(video_url)
        # re_patter_0 = """url: "(https://vod.hjbfq1.com/.*?)","""
        # re_patter_1 = """url: "(https://.*?index.m3u8)","""
        re_patter = """url: "(https://.*?index.m3u8)","""

        m3u8_url_pre = re.findall(re_patter, resp.text)
        if m3u8_url_pre:
            m3u8_url_pre = m3u8_url_pre[0]
        else:
            raise Exception("have no u3m8")

        resp = requests.get(m3u8_url_pre)
        m3u8_url_list = []
        m3u8_base_url = re.findall("(https://.*?\.com)", m3u8_url_pre)[0]
        for line in resp.text.split('\n'):
            "/20210812/vJlFYlIY/500kb/hls/index.m3u8"
            if line.endswith("m3u8"):
                m3u8_url_list.append(m3u8_base_url + line)
        print(m3u8_url_list)
        return m3u8_url_list, m3u8_base_url

    def download_process_m3u8(self, m3u8_url_list, m3u8_base_url, base_dir, name):
        """
        预下载，获取m3u8文件，读出ts链接，并写入文档
        :param m3u8_url_list:
        :param m3u8_base_url: 当ts文件链接不完整时，需拼凑
        :param base_dir:
        :param name:
        :return:
        """
        flag = False
        m3u8_url = m3u8_text = ""
        for m3u8_url in m3u8_url_list:
            resp = requests.get(m3u8_url, headers=headers)
            m3u8_text = resp.text
            if resp.status_code == 200:
                flag = True
                break
        if not flag:
            sql = "update dstv set m3u8_url_status='0' where name='{}'".format(name)
            mysql.update(sql)
            return False, False

        if m3u8_url.startswith("https://vip"):
            sql = "update dstv set m3u8_url='{}',m3u8_url_status='{}'  where name='{}'".format(m3u8_url, '1', name)
            mysql.update(sql)
            return False, False

        sql = "update dstv set m3u8_url='{}',m3u8_url_status='{}'  where name='{}'".format(m3u8_url, '200', name)
        mysql.update(sql)

        # 按行拆分m3u8文档
        ts_queue = Queue(10000)
        concatfile = '{}/{}.m3u8'.format(base_dir, name)
        if os.path.exists(concatfile):
            os.remove(concatfile)
        with open(concatfile, 'a+') as f:
            # 找到文档中含有ts字段的行
            lines = m3u8_text.split('\n')
            for i, line in enumerate(lines):
                if '.ts' in line:
                    if 'http' in line:
                        ts_queue.put(line)
                    else:
                        line = m3u8_base_url + line
                        ts_queue.put(line)

                    ts_filename = re.search('([a-zA-Z0-9-_]+\.ts)', line).group(1).strip()
                    # 一定要先写文件，因为线程的下载是无序的，文件无法按照123456。。。去顺序排序，而文件中的命名也无法保证是按顺序的
                    # 这会导致下载的ts文件无序，合并时，就会顺序错误，导致视频有问题。
                    f.write("{}\n".format(ts_filename))
                    print("\r", '文件写入中', i, "/", len(lines), end="", flush=True)
                else:
                    f.write(line + "\n")
        return ts_queue, concatfile

    def download_ts(self, ts_queue, base_dir):
        """
        执行下载任务
        :param ts_queue:
        :param headers:
        :param base_dir:
        :return:
        """
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN, zhq=0.9',
            'sec-ch-ua': 'Not A;Brand,v = 99, Chromium;v = 99, Google Chrome;v=99',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': "Windows",
            'sec-fetch-dest': 'sec-fetch-dest',
            'sec-fetch-mode': 'sec-fetch-mode',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
        }

        while not ts_queue.empty():
            url = ts_queue.get()
            filename = re.search('([a-zA-Z0-9-_]+\.ts)', url).group(1).strip()
            try:
                requests.packages.urllib3.disable_warnings()
                r = requests.get(url, stream=True, headers=headers, verify=False)
                with open('{}/{}'.format(base_dir, filename), 'wb') as fp:
                    for chunk in r.iter_content(1024):
                        if chunk:
                            fp.write(chunk)
                print("\r", '任务文件 ', filename, ' 下载成功', end="", flush=True)
            except Exception as e:
                logger.exception('任务文件 ', filename, ' 下载失败')
                ts_queue.put(url)

    def merge(self, concatfile, name, base_dir):
        """
        视频合并，使用ffmpeg
        :param concatfile:
        :param name:
        :param base_dir:
        :return:
        """
        try:
            ffmpeg = "C:\\Users\\Administrator\\Downloads\\ffmpeg-2022-01-17-git-dcc9454ab9-essentials_build\\bin\\ffmpeg.exe"
            cmd_ffmpeg_cut = ffmpeg + """ -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -ss 00:00:00.002 -c copy "{}"
            """
            out_path = 'video/{}.mp4'.format(name)
            out_path_zip = 'video_rar/{}.rar'.format(name)
            command = cmd_ffmpeg_cut.format(concatfile, out_path)
            print(command)
            os.system(command)
            zip_encrypt(out_path, out_path_zip)
            print('视频合并完成')
        except:
            print('合并失败')

    def remove(self, concatfile, base_dir):
        try:
            for line in open(concatfile):
                if '.ts' in line:
                    line = re.search('(.*?\.ts)', line).group(1).strip()
                    os.remove('{}/{}'.format(base_dir, line))
            os.remove('{}'.format(concatfile))
        except:
            logger.exception("文件删除失败")

    def factory(self, name="name", video_url="https://yiyi.55zuiday.com/ppvod/70B5A6E3A150A99882E28EC793CAF519.m3u8"):
        """
        多线程下载合并 m3u8 视频
        :param name: 视频名称
        :param url: m3u8 地址
        :param base_url:
        :return:
        """
        base_dir = "cache"
        start = datetime.datetime.now().replace(microsecond=0)

        m3u8_url_list, m3u8_base_url = self.get_m3u8_url(video_url)

        # 第一步，下载 m3u8 文件
        ts_queue, concatfile = self.download_process_m3u8(m3u8_url_list, m3u8_base_url, base_dir, name)

        if not ts_queue:
            return
        # 第二步，根据数量来开线程数，每五个元素一个线程,最大开到50个
        num = ts_queue.qsize()
        if num > 10:
            t_num = 10
        elif num > 5:
            t_num = num // 5
        else:
            t_num = 1

        threads = []
        for i in range(t_num):
            t = threading.Thread(target=self.download_ts, name='th-' + str(i), kwargs={'ts_queue': ts_queue, 'base_dir': base_dir})
            t.setDaemon(True)
            threads.append(t)
        for t in threads:
            time.sleep(0.4)
            t.start()
        for t in threads:
            t.join()

        end = datetime.datetime.now().replace(microsecond=0)

        # 第三步，合并
        print(concatfile, name, base_dir)
        self.merge(concatfile, name, base_dir)

        sql = "update dstv set have_download='{}'  where name='{}'".format('200', name)
        mysql.update(sql)

        # 第四部，删除
        self.remove(concatfile, base_dir)
        over = datetime.datetime.now().replace(microsecond=0)
        print('下载耗时：{}，合并耗时：{}，总耗时：{}。'.format(str(end - start), str(over - end), str(over - start)))

    def main(self):
        """
        status
            0: 获取失败
            1：下载ts 文件 为1
            200：获取成功
        :return:
        """
        sql = "SELECT name, video_url, video_url_base, video_type FROM dstv where video_type like '乐播%' and have_download is null and m3u8_url_status is null LIMIT 0, 10; "
        for i in mysql.select(sql):
            name, video_url, video_url_base, video_type = i
            # video_url = "/detail?pid=0&id=327191"
            video_url = video_url_base + video_url
            print(name, video_url)
            self.factory(name, video_url)


if __name__ == "__main__":
    # save_url()
    Download_u3m8_ds().main()
