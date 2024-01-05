# -*- coding: utf-8 -*-
import time
import random
import requests
import datetime
import logging
import pymysql

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class MySQLLocal(object):

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
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql, sql_parameter)
            data = cursor.fetchall()
            cursor.close()
            return data
        except Exception as e:
            logger.exception(e)
            return []

        finally:
            if cursor is not None:
                cursor.close()

    def exec_sql(self, sql, data=None):
        cursor = None
        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.execute(sql, data)
            self.conn.commit()
            return True
        except Exception as e:
            logger.exception(e)
            if self.conn is not None:
                self.conn.rollback()
            return False

        finally:
            if cursor is not None:
                cursor.close()

    def update(self, sql, data=None):
        return self.exec_sql(sql, data)

    def insert(self, sql, data=None):
        return self.exec_sql(sql, data)

    def delete(self, sql, data=None):
        return self.exec_sql(sql, data)

    def truncate_table(self, sql=None, data=None):
        return self.exec_sql(sql, data)

    def insert_many_items(self, sql=None, data=None):
        cursor = None

        try:
            self.conn.ping(reconnect=True)
            cursor = self.conn.cursor()
            cursor.executemany(sql, data)
            self.conn.commit()
        except Exception as e:
            logger.exception(e)
            if self.conn is not None:
                self.conn.rollback()
        finally:
            if cursor is not None:
                cursor.close()

    def __del__(self):
        try:
            self.conn.close()
        except Exception as e:
            logger.exception("close db error")


def get_url_list():
    url_list = {}
    user = "root"
    port = "3306"
    host = "81.70.160.146"
    passwd = "cavWib-pamwyc-6kotro"
    db = "lp"
    mysql = MySQLLocal(host, port, user, passwd, db)
    ret_sql = mysql.select("select url from csdn")
    for i in ret_sql:
        url_list[i[0]] = 1
    return url_list


url_list = {
    'http://blog.csdn.net/fenglepeng/article/details/121117887': 200,  # 深度学习之 OHEM （Online Hard Example Mining）
    'http://blog.csdn.net/fenglepeng/article/details/121107271': 200,  # 深度学习之双线性插值（Bilinear interpolation）
    'http://blog.csdn.net/fenglepeng/article/details/121097088': 200,  # 深度学习之 DCN（Deformable Convolution）-可变形卷积
    'http://blog.csdn.net/fenglepeng/article/details/121013782': 300,  # 深度学习之 Cascade R-CNN
    'http://blog.csdn.net/fenglepeng/article/details/120825214': 200,  # 深度学习之 soft-NMS
    'http://blog.csdn.net/fenglepeng/article/details/120724125': 300,  # 深度学习之 RetinaNet
    'http://blog.csdn.net/fenglepeng/article/details/108760047': 20,  # 递归神经网络变形之 （Long Short Term Memory，LSTM）
    'http://blog.csdn.net/fenglepeng/article/details/117323619': 20,  # 深度学习之生成式对抗网络 GAN（Generative Adversarial Networks）
    'http://blog.csdn.net/fenglepeng/article/details/117368102': 20,  # 深度学习之 Region proposal+CNN（RCNN）
    'http://blog.csdn.net/fenglepeng/article/details/117412366': 20,  # 深度学习之边框回归(Bounding Box Regression)
    'http://blog.csdn.net/fenglepeng/article/details/117468724': 20,  # 深度学习之检测算法 SSD（Single Shot MultiBox Detector）
    'http://blog.csdn.net/fenglepeng/article/details/117532615': 20,  # 深度学习之卷积神经网络 AlexNet
    'http://blog.csdn.net/fenglepeng/article/details/117712016': 20,  # 深度学习之卷积神经网络 ZF Net
    'http://blog.csdn.net/fenglepeng/article/details/117713426': 20,  # 深度学习之卷积神经网络 GoogleNet
    'http://blog.csdn.net/fenglepeng/article/details/117714126': 20,  # 深度学习之卷积神经网络 VGGNet
    'http://blog.csdn.net/fenglepeng/article/details/117714368': 20,  # 深度学习之卷积神经网络 ResNet
    'http://blog.csdn.net/fenglepeng/article/details/117898968': 20,  # 深度学习之 RPN（RegionProposal Network）
    'http://blog.csdn.net/fenglepeng/article/details/117885129': 20,  # 深度学习之 ROI Pooling
    'http://blog.csdn.net/fenglepeng/article/details/117871797': 20,  # 深度学习之非极大值抑制（Non-maximum suppression，NMS）
    'http://blog.csdn.net/fenglepeng/article/details/117870253': 20,  # 深度学习之 hard negative mining （难例挖掘）
    'http://blog.csdn.net/fenglepeng/article/details/118083107': 20,  # 深度学习之 TensorRT
    'http://blog.csdn.net/fenglepeng/article/details/118524682': 20,  # 深度学习目标检测之 YOLO v1
    'http://blog.csdn.net/fenglepeng/article/details/118543497': 20,  # 深度学习之 深度学习之 SSD(Single Shot MultiBox Detector)
    'http://blog.csdn.net/fenglepeng/article/details/108594997': 10,  # RNN
    'http://blog.csdn.net/fenglepeng/article/details/108465522': 10,  # 预训练和加载
    'http://blog.csdn.net/fenglepeng/article/details/108532969': 10,  # 验证码识别
    'http://blog.csdn.net/fenglepeng/article/details/108452769': 10,  # 手写
    'http://blog.csdn.net/fenglepeng/article/details/106077002': 10,  # 卷积1
    'http://blog.csdn.net/fenglepeng/article/details/106208923': 10,  # 卷积2
    'http://blog.csdn.net/fenglepeng/article/details/106209038': 10,  # 卷积3
    'http://blog.csdn.net/fenglepeng/article/details/104829873': 10,  # 激活函数
    'http://blog.csdn.net/fenglepeng/article/details/106052876': 10,  # 深度学习之 RBF神经网络
    'http://blog.csdn.net/fenglepeng/article/details/106024772': 10,  # 神经网络之 BP 算法
    'http://blog.csdn.net/fenglepeng/article/details/106022640': 10,  # 深度学习之概述

    'http://blog.csdn.net/fenglepeng/article/details/111323841': 20,  # markdown语法入门

    'http://blog.csdn.net/fenglepeng/article/details/80182245': 20,  # Docker 精通之入门
    'http://blog.csdn.net/fenglepeng/article/details/80183123': 20,  # Docker 精通之微服务
    'http://blog.csdn.net/fenglepeng/article/details/80185574': 20,  # Docker 精通之常用命令
    'http://blog.csdn.net/fenglepeng/article/details/104829762': 20,  # Docker 精通之 Dockerfile
    'http://blog.csdn.net/fenglepeng/article/details/114835890': 20,  # Docker 精通之 docker-compose


    'http://blog.csdn.net/fenglepeng/article/details/114918566': 20,  # kafka 命令行命令大全
    'http://blog.csdn.net/fenglepeng/article/details/111525212': 20,  # kafka 异常
    'http://blog.csdn.net/fenglepeng/article/details/110861258': 20,  # kafka 异常
    'http://blog.csdn.net/fenglepeng/article/details/114532420': 20,  # kafka 日志相关配置
    'http://blog.csdn.net/fenglepeng/article/details/109748696': 10,  # kafka 自动提交 和 手动提交
    'http://blog.csdn.net/fenglepeng/article/details/109454576': 10,  # python-kafka 常用 api 汇总
    'http://blog.csdn.net/fenglepeng/article/details/109330002': 10,  # kafka 安装
    'http://blog.csdn.net/fenglepeng/article/details/109328832': 10,  # kafka 入门


    'http://blog.csdn.net/fenglepeng/article/details/111318059': 20,  # Python 内置函数之 open (文件操作)
    'http://blog.csdn.net/fenglepeng/article/details/110947667': 20,  # python 内置模块 subprocess
    'http://blog.csdn.net/fenglepeng/article/details/114933182': 20,  # Python 内置模块之 ConfigParser - 解析 ini 文件
    'http://blog.csdn.net/fenglepeng/article/details/117301960': 120,  # Python 第三方模块之 numpy.random
    'http://blog.csdn.net/fenglepeng/article/details/116998236': 120,  # Python 第三方模块之 imgaug （图像增强）
    'http://blog.csdn.net/fenglepeng/article/details/117463963': 20,  # python 第三方模块之 pandas 操作 excel


    'http://blog.csdn.net/fenglepeng/article/details/112765561': 20,  # Python 第三方库之 beautifulsoup（bs4）- 解析 HTML
    'http://blog.csdn.net/fenglepeng/article/details/103768230': 20,  # Python 第三方模块之 ElementTree（ET）- 解析XML文件
    'http://blog.csdn.net/fenglepeng/article/details/112767007': 20,  # Python 第三方模块之 lxml - 解析 HTML 和 XML 文件
    'http://blog.csdn.net/fenglepeng/article/details/112331659': 20,  # python 第三方模块 yaml - 处理 YAML （专门用来写配置文件的语言）
    'http://blog.csdn.net/fenglepeng/article/details/113392016': 20,  # Python 第三方模块之 psutil - 获取系统运行的进程和系统利用率信息
    'http://blog.csdn.net/fenglepeng/article/details/114281289': 20,  # Python 第三方模块之 selenium - 模拟操作 Chrome 浏览器
    'http://blog.csdn.net/fenglepeng/article/details/114592795': 20,  # flask-SQLAlchemy 使用 session.commit() 处理异常回滚
    'http://blog.csdn.net/fenglepeng/article/details/119252450': 20,  # Python 包管理之 poetry
    'http://blog.csdn.net/fenglepeng/article/details/119296632': 20,  # Python 之打包工具 setup.py


    'http://blog.csdn.net/fenglepeng/article/details/110923847': 20,  # git
    'http://blog.csdn.net/fenglepeng/article/details/104733553': 20,  # git 命令详解和常见问题解决
    'http://blog.csdn.net/fenglepeng/article/details/112041312': 20,  # GitHub 搜索技巧


    'http://blog.csdn.net/fenglepeng/article/details/112546265': 20,  # 前端之 form 详解
    'http://blog.csdn.net/fenglepeng/article/details/109853977': 20,  # 前端之 JavaScript 常用数据类型和操作
    'http://blog.csdn.net/fenglepeng/article/details/113338093': 20,  # HTTP POST 发送数据的参数 application/x-www-form-urlencoded、multipart/form-data、text/plain
    'http://blog.csdn.net/fenglepeng/article/details/114526779': 20,  # 前端之使用 POST 提交数据并跳转


    'http://blog.csdn.net/fenglepeng/article/details/110797565': 20,  # requirement


}
url_list = get_url_list()
url_count = {i: 0 for i in url_list.keys()}


def get_url(data):
    total = sum(data.values())
    rad = random.randint(1, total)
    cur_total = 0
    for k, v in data.items():
        cur_total += v
        if rad <= cur_total:
            url_count[k] += 1
            return k


def get_header():
    phone_agent_list = [
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        # "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    ]
    user_agent_list = [
        'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0)',
        'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT6.0)',
        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
        'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
        'Mozilla/4.0(compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0(Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
        'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36',
        'Mozilla/5.0(Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36',

        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        "Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0"
    ]
    referer_list = [
        'https://blog.csdn.net/fenglepeng',
        'http://blog.csdn.net/',
        'http://www.baidu.com/',
    ]

    header = {
        'User-Agent': random.choice(user_agent_list),
        'Referer': random.choice(referer_list),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Connection': 'keep-alive',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    return header


def main():
    n = 1
    while True:
        ret = requests.get(get_url(url_list), headers=get_header())
        logger.warning("id:{}\t,url:{}\t,code:{}\t,count:{}".format(n, ret.url, ret.status_code,  url_count))
        time.sleep(random.randint(30, 100))
        n += 1
        now_hour = datetime.datetime.now().hour
        if now_hour < 8 or now_hour > 22:
            time.sleep(60 * 60)


if __name__ == "__main__":
    main()

