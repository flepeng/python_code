# -*- coding:utf-8 -*-
"""
    @Time  : 2022/2/22  14:39
    @Author: Feng Lepeng
    @File  : download_merge_m3u8.py
    @Desc  : 多线程下载合并 m3u8 类型视屏流
"""
import datetime
import os
import re
import threading
import time
import requests
import logging
from queue import Queue


logger = logging.getLogger()

headers = {
    'referer': 'https://yiyi.55zuiday.com/share/wVuAcJFy1tMy4t0x',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}


class DownloadMergeU3M8():

    def get_m3u8_url(self, video_url):
        """
        根据 video_url 获取 m3u8 url
        :param video_url:
        :return: m3u8 url list， m3u8 base url
        """
        resp = requests.get(video_url)
        re_patter = """url: "(https://.*?index.m3u8)","""
        m3u8_url_pre = re.findall(re_patter, resp.text)
        if m3u8_url_pre:
            m3u8_url_pre = m3u8_url_pre[0]
        else:
            return [], ""

        resp = requests.get(m3u8_url_pre)
        m3u8_url_list = []
        m3u8_base_url = re.findall("(https://.*?\.com)", m3u8_url_pre)[0]
        for line in resp.text.split('\n'):
            # /20210812/vJlFYlIY/500kb/hls/index.m3u8
            if line.endswith("m3u8"):
                m3u8_url_list.append(m3u8_base_url + line)

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
        if not m3u8_url_list:
            logger.info("该视屏无法访问。")
            return False, False, False

        # 对应的 m3u8 地址是否能访问
        flag = False
        m3u8_text = ""
        for m3u8_url in m3u8_url_list:
            resp = requests.get(m3u8_url, headers=headers)
            m3u8_text = resp.text
            if resp.status_code == 200:
                flag = True
                break
        if not flag:
            return False, False, False

        logger.info(f"{m3u8_url} 可以访问")

        # 按行拆分m3u8文档
        ts_queue = Queue(10000)
        m3u8_file = '{}/{}.m3u8'.format(base_dir, name)
        if os.path.exists(m3u8_file):
            os.remove(m3u8_file)

        with open(m3u8_file, 'a+') as f:
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
                elif re.findall('URI="(.*?/key.key")', line):
                    old = re.findall('URI="(.*?/key.key")', line)[0]
                    line = line.replace(old, m3u8_base_url + old)
                    print(line)
                    f.write(line + "\n")
                else:
                    f.write(line + "\n")
        return ts_queue, m3u8_file, m3u8_url

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
            except Exception:
                logger.exception('任务文件 ', filename, ' 下载失败')
                ts_queue.put(url)

    def merge(self, m3u8_file, name, video_base_dir):
        """
        视频合并，使用ffmpeg
        :param concatfile:
        :param name:
        :param base_dir:
        :return:
        """
        try:
            ffmpeg = "C:\\Users\\Administrator\\Downloads\\ffmpeg-2022-01-17-git-dcc9454ab9-essentials_build\\bin\\ffmpeg.exe"
            cmd_ffmpeg_cut = ffmpeg + """ -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp,https,tls" -i "{}" -ss 00:00:00.002 -c copy "{}"
            """
            out_path = '{}/video/{}.mp4'.format(video_base_dir, name)
            command = cmd_ffmpeg_cut.format(m3u8_file, out_path)
            logger.info(command)
            os.system(command)
            logger.info('视频合并完成')
            return out_path
        except Exception:
            logger.exception("视频合并失败")
            return False

    def remove(self, m3u8_file, base_dir):
        try:
            for line in open(m3u8_file):
                if '.ts' in line:
                    line = re.search('(.*?\.ts)', line).group(1).strip()
                    os.remove('{}/{}'.format(base_dir, line))
            os.remove('{}'.format(m3u8_file))
        except:
            logger.exception("文件删除失败")

    def factory(self, name="name", video_url="", m3u8_url_list="https://yiyi.55zuiday.com/ppvod/70B5A6E3A150A99882E28EC793CAF519.m3u8", m3u8_base_url="https://yiyi.55zuiday.com"):
        """
        多线程下载合并 m3u8 视频
        :param name: 视频名称
        :param video_url: 视屏 地址
        :param m3u8_url_list: m3u8 地址列表
        :param m3u8_base_url: m3u8 文件 base url
        :return:
        """
        base_dir = "cache"
        video_base_dir = "cache"
        start = datetime.datetime.now().replace(microsecond=0)

        if not m3u8_url_list:
            m3u8_url_list, m3u8_base_url = self.get_m3u8_url(video_url)

        if not m3u8_url_list:
            raise Exception("没有可用的 m3u8 地址")

        # 第一步，下载 m3u8 文件
        logger.info("download m3u8 ts start...")
        ts_queue, m3u8_file, m3u8_url = self.download_process_m3u8(m3u8_url_list, m3u8_base_url, base_dir, name)

        if not ts_queue:
            raise Exception("download m3u8 fail...")

        # 第二步，根据数量来开线程数, 最大开到10个
        logger.info("download video start...")
        num = ts_queue.qsize()
        t_num = num // 2 if num < 10 else 10

        threads = []
        for i in range(t_num):
            t = threading.Thread(target=self.download_ts, name='th-' + str(i),
                                 kwargs={'ts_queue': ts_queue, 'base_dir': base_dir})
            t.setDaemon(True)
            threads.append(t)

        for t in threads:
            t.start()
            time.sleep(0.4)

        for t in threads:
            t.join()

        end = datetime.datetime.now().replace(microsecond=0)

        # 第三步，合并
        logger.info("merge start...")
        out_path = self.merge(m3u8_file, name, video_base_dir)

        if not out_path:
            raise Exception("download m3u8 fail...")

        # 第四部，删除
        self.remove(m3u8_file, base_dir)
        over = datetime.datetime.now().replace(microsecond=0)
        print('下载耗时：{}，合并删除耗时：{}，总耗时：{}。'.format(str(end - start), str(over - end), str(over - start)))


if __name__ == '__main__':
    DownloadMergeU3M8().factory()
