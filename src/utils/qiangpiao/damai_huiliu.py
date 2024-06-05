# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2023/10/30 14:52
    @File   : adb_util.py
    @Desc   :
"""
import time
import random
import uiautomator2 as u2
from threading import Thread
from utils.qiangpiao.logging_util import logger


# 连接手机的USB进行连接(安卓模拟器和真机都可以）必须开启USB调试模，id 为 adb devices 命令中得到的设备 id
d = u2.connect_usb("c9c32495")
d.screen_on()
d.implicitly_wait(60*5)  # 等待时长，时间为秒

# 页面设置
max_flush_time = 20  # 努力刷新最大次数


# 定义滑块偏移量
offsetX = 12  # 滑块横坐标偏移量
offsetY = 25  # 滑块纵坐标偏移量
swipeLength = 1200  # 滑块的滑动距离
swipeTime = random.randint(100, 200)  # 多少毫秒内滑完滑块


def backend_immediately_buy():
    """
    后台进程：提交订单
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：立即购买"))
    while True:
        d(text="立即购买").click()
        logger.info("点击立即购买")


def backend_sure():
    """
    后台进程：确定
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：确定"))
    while True:
        element = d(resourceId="cn.damai:id/tv_price")
        if element.exists():
            if element.get_text() != "0":
                d(text="确定").click()
                logger.info("点击确定")
        time.sleep(0.1)


def backend_flush():
    """
    后台进程：努力刷新
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：努力刷新"))

    while True:
        for i in range(1, max_flush_time):
            d(text="努力刷新").click()
            logger.info("努力刷新第{}次".format(i))
        logger.info("努力刷新页面跳转到前一页")
        d.press("back")


def backend_sliper():
    """
    后台进程：滑块
    :return:
    """

    """
    {
        'bounds': {'bottom': 921, 'left': 17, 'right': 523, 'top': 811},
        'childCount': 0,
        'className': 'android.widget.Button',
        'contentDescription': None,
        'packageName': 'com.github.uiautomator',
        'resourceName': 'com.github.uiautomator:id/development_settings',
        'text': '开发者选项',
        'visibleBounds': {'bottom': 921, 'left': 17, 'right': 523, 'top': 811},
        'checkable': False,
        'checked': False,
        'clickable': True,
        'enabled': True,
        'focusable': True,
        'focused': False,
        'longClickable': False,
        'scrollable': False,
        'selected': False
    }
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：滑块启动"))

    while True:
        element = d(text="向右滑动验证")
        if element.exists():
            x = element.bounds()[0]
            y = element.bounds()[1]
            x_end = element.bounds()[2]
            y_end = element.bounds()[3]
            logger.info("找到滑块坐标(x:{}, y:{})，开始尝试滑动".format(x, y))
            d.swipe(x+offsetX, y + offsetY, x + swipeLength, y + y+offsetY*2, swipeTime)
        time.sleep(500)


def backend_click_submit_order():
    """
    后台进程：提交订单
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：最后一步提交订单"))
    while True:
        d(text="提交订单").click()
        logger.info("点击提交订单")


def backend_continue_try():
    """
    后台进程：继续尝试
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：继续尝试"))
    while True:
        d(text="继续尝试").click()
        logger.info("点击继续尝试")


def backend_i_know():
    """
    后台进程：我知道了
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：我知道了"))
    while True:
        d(text="我知道了").click()
        logger.info("点击我知道了")


def main():
    # todo: 验证失败，点击框体重试
    logger.info("{} {}".format("*"*20, "开始"))

    t = Thread(target=backend_immediately_buy, args=())  # 立即购买
    t.start()
    t = Thread(target=backend_sure, args=())  # 确认
    t.start()

    t = Thread(target=backend_flush, args=())  # 努力刷新，这是点击确定之后会出现的页面
    t.start()
    t = Thread(target=backend_sliper, args=())  # 滑块验证，这是点击确定之后会出现的页面
    t.start()

    t = Thread(target=backend_click_submit_order, args=())  # 提交订单
    t.start()
    t = Thread(target=backend_continue_try, args=())  # 继续尝试，这是点击提交订单时会出现的页面
    t.start()
    t = Thread(target=backend_i_know, args=())  # 我知道了，这是点击提交订单时会出现的页面
    t.start()
    while True:
        time.sleep(60*10)


if __name__ == "__main__":
    main()
    random.randint(2, 10)

