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

test = True
name = "薛之谦"
day = "2023-11-11 周六 19:00"
price = "内场1717元"
num = "2张"
start_time = time.time()

# 页面设置
max_flush_time = 20  # 努力刷新最大次数

# 定义滑块偏移量
offsetX = 12  # 滑块横坐标偏移量
offsetY = 25  # 滑块纵坐标偏移量
swipeLength = 1200  # 滑块的滑动距离
swipeTime = random.randint(100, 200)  # 多少毫秒内滑完滑块


def open_dm(close=False):
    d.press("home")
    if close:
        d.app_stop("cn.damai", wait=True, timeout=100)

    # d(text="大麦").click()
    d.app_start("cn.damai", wait=True)


def click_confirm_butten():
    """
    点击确认按钮
    :return:
    """
    confirm_butten = d(resourceId="cn.damai:id/damai_theme_dialog_confirm_btn")
    try:
        if confirm_butten.get_text(timeout=1) == "确认并知悉":
            confirm_butten.click()
    except Exception as e:
        pass


def click_buy_first():
    text = "立即购买"
    d(text=text).click()


def click_buy():
    logger.info("{} {}".format("*"*20, "第一步：点击立即预订"))
    text = "缺货登记" if test else "立即预订"
    buy_butten = d(resourceId="cn.damai:id/tv_left_main_text")
    if buy_butten.get_text() == text:
        buy_butten.click()
        print(1, time.time() - start_time)
        time.sleep(1)
        return True
    else:
        return False


def click_day_and_price_1():
    sure_element = d(text="确定")
    print(2, time.time() - start_time)
    right_price_elemet = d(text=price)

    right_price_elemet.click()
    print(5, time.time() - start_time)
    if sure_element.exists:
        return True
    else:
        d.press('back')
        return False


def click_day_and_price_2():
    right_day_element = None
    other_day_element = []
    right_price_elemet = None
    sure_element = d(text="确定")
    day_butten = d(resourceId="cn.damai:id/item_text")
    print(2, time.time() - start_time)
    for i in day_butten:
        print(i.get_text())
        if day in i.get_text():
            right_day_element = i
        elif "周" in i.get_text():
            other_day_element.append(i)
        elif price in i.get_text():
            right_price_elemet = i
    print(22, time.time() - start_time)
    for i in range(10):
        right_day_element.click()
        print(3, time.time() - start_time)
        # day_butten = d(resourceId="cn.damai:id/item_text")
        # print(4, time.time() - start_time)
        # for i in day_butten:
        #     if price in i.get_text():
        #         i.click()
        right_price_elemet.click()

        if sure_element.exists:
            return True
        print(5, time.time() - start_time)

        if other_day_element:
            other_day_element[0].click()
            print(6, time.time() - start_time)
        else:
            d.press('back')
            return False


def click_day_and_price_21():
    other_day_element = []

    right_day_element = d(text=day)
    right_price_elemet = d(text=price)
    right_day_element.click()

    sure_element = d(text="确定")
    day_butten = d(resourceId="cn.damai:id/item_text")
    print(2, time.time() - start_time)
    for i in day_butten:
        print(i.get_text())
        if "周" in i.get_text():
            other_day_element.append(i)
    print(22, time.time() - start_time)
    for i in range(10):
        right_day_element.click()
        print(3, time.time() - start_time)
        # day_butten = d(resourceId="cn.damai:id/item_text")
        # print(4, time.time() - start_time)
        # for i in day_butten:
        #     if price in i.get_text():
        #         i.click()
        right_price_elemet.click()

        if sure_element.exists:
            return True
        print(5, time.time() - start_time)

        if other_day_element:
            other_day_element[0].click()
            print(6, time.time() - start_time)
        else:
            break

    d.press('back')
    return False


def click_day_and_price_by_text():
    day_butten = d(text=day)
    print(2, time.time() - start_time)
    day_butten.click()
    # time.sleep(0.5)
    print(3, time.time() - start_time)
    price_butten = d(text=price)
    print(4, time.time() - start_time)
    price_butten.click()
    print(5, time.time() - start_time)


def click_day_and_price():
    logger.info("{} {}".format("*" * 20, "第二步：选择场次和票价"))
    return click_day_and_price_21()


def backend_click_sure_order():
    logger.info("{} {}".format("*" * 20, "后台进程启动：确认"))
    current_num_element = d(resourceId="cn.damai:id/tv_num")
    print(current_num_element.get_text())
    if current_num_element.get_text() != num:
        add_element = d(resourceId="cn.damai:id/img_jia")
        for i in range(0, 6):
            add_element.click()
            print(current_num_element.get_text())
            if current_num_element.get_text() == num:
                break
    while True:
        d(resourceId="cn.damai:id/tv_num")
        butten = d(text="确定")
        butten.click()


def backend_click_submit_order():
    logger.info("{} {}".format("*" * 20, "最后一步：提交订单"))
    while True:
        d(text="提交订单").click()


def backend_i_know():
    """
    后台进程：我知道了
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：我知道了"))
    while True:
        d(text="我知道了").click()
        logger.info("点击我知道了")


def backend_continue_try():
    """
    后台进程：继续尝试
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：继续尝试"))
    while True:
        d(text="继续尝试").click()
        logger.info("点击继续尝试")


def backend_flush():
    """
    后台进程：努力刷新
    :return:
    """
    logger.info("{} {}".format("*" * 20, "后台进程启动：努力刷新"))

    while True:
        for i in range(max_flush_time):
            logger.info("努力刷新第{}次".format(i))
            d(text="努力刷新").click()
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
    :return:
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


def main():
    # todo: 验证失败，点击框体重试
    logger.info("{} {}".format("*"*20, "开始"))

    t = Thread(target=backend_flush, args=())  # 努力刷新，这是点击确定之后会出现的页面
    t.start()
    t = Thread(target=backend_sliper, args=())  # 滑块验证，这是点击确定之后会出现的页面
    t.start()

    # t = Thread(target=backend_click_sure_order, args=())  # 确认
    # t.start()

    t = Thread(target=backend_click_submit_order, args=())  # 提交订单
    t.start()
    t = Thread(target=backend_continue_try, args=())  # 继续尝试，这是点击提交订单时会出现的页面
    t.start()
    t = Thread(target=backend_i_know, args=())  # 我知道了，这是点击提交订单时会出现的页面
    t.start()



    # open_dm()
    d(text="立即购买").click()
    d(text="确定").click()
    flag = False
    while not flag:
        flag = click_day_and_price()
        if not flag:
            d.swipe_ext("down")
            ret = click_buy()


if __name__ == "__main__":
    # main()
    print(random.randint(2, 10))