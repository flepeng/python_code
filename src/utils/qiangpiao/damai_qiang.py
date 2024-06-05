# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2023/10/30 14:52
    @File   : adb_util.py
    @Desc   :
"""
import time
import uiautomator2 as u2
from threading import Thread
from logging import getLogger

logger = getLogger(__name__)

# 连接手机的USB进行连接(安卓模拟器和真机都可以）必须开启USB调试模，id 为 adb devices 命令中得到的设备 id
# d = u2.connect_usb("127.0.0.1:5555")
d = u2.connect_usb("c9c32495")
d.screen_on()

test = True
name = "薛之谦"
day = "2023-11-11 周六 19:00"
price = "内场1717元"
num = "2张"
start_time = time.time()

tijiao_page = ["努力刷新", "我知道了", ""]


def open_dm(close=False):
    d.press("home")
    if close:
        d.app_stop("cn.damai", wait=True)

    # d(text="大麦").click()
    d.app_start("cn.damai", wait=True)


# d(resourceId="cn.damai:id/channel_search_text").click()  # 搜索
# d(resourceId="cn.damai:id/header_search_v2_input").set_text(name)
# d(resourceId="cn.damai:id/tv_word", text=name).click()  # 点击
# d(resourceId="cn.damai:id/ll_project_right").click()  # 点击第一个
# d(resourceId="cn.damai:id/damai_theme_dialog_confirm_btn").click()
# d(resourceId="cn.damai:id/trade_project_detail_purchase_status_bar_container_fl").click()


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
    text = "缺货登记" if test else "立即预订"
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


def backend_wozhidao():
    logger.info("{} {}".format("*" * 20, "后台进程启动：我知道了"))
    while True:
        d(text="我知道了").click()


def backend_jixuchangshi():
    logger.info("{} {}".format("*" * 20, "后台进程启动：继续尝试"))
    while True:
        d(text="继续尝试").click()


def backend_nulishuaxin():
    logger.info("{} {}".format("*" * 20, "后台进程启动：努力刷新"))
    while True:
        d(text="努力刷新").click()


def main():
    logger.info("{} {}".format("*"*20, "开始"))
    t = Thread(target=backend_wozhidao, args=())
    t.start()
    t = Thread(target=backend_click_sure_order, args=())
    t.start()
    t = Thread(target=backend_jixuchangshi, args=())
    t.start()
    t = Thread(target=backend_nulishuaxin, args=())
    t.start()
    t = Thread(target=backend_click_submit_order, args=())
    t.start()

    # open_dm()
    # click_buy_first()
    flag = False
    flag_submit = False
    while not flag:
        flag = click_day_and_price()
        if not flag:
            d.swipe_ext("down")
            ret = click_buy()


if __name__ == "__main__":
    main()
