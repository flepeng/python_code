# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2024/8/30 17:11
    @File   : message_color_util.py
    @Desc   : 把消息在输出的时候加上颜色和背景色
"""


class MessageColor(object):
    format_flag = False

    @classmethod
    def handle(cls, message: str = None, foreground_color: str = "", background_color: str = "",
               code: str = "0") -> str:
        # \033[代码;前景色;背景色m 字符串 \033[0m
        code = code + ";" if code else ""
        foreground_color = foreground_color + ";" if foreground_color else ""
        background_color = background_color + ";" if background_color else ""
        expression = code + foreground_color + background_color
        if expression:
            expression = expression.strip(";") + "m"
        if cls.format_flag:
            # message = message.center(20, " ").center(100, "=")
            message = "{:^100}".format(message)
        return f"\033[{expression}{message}\033[0m"

    @classmethod
    def debug(cls, message: str = None) -> str:
        return cls.handle(message, "30", "47", "1")

    @classmethod
    def info(cls, message: str = None) -> str:
        return cls.handle(message, "30", "42", "1")

    @classmethod
    def warn(cls, message: str = None) -> str:
        # 黑字黄底
        return cls.handle(message, "30", "43", "1")

    @classmethod
    def error(cls, message: str = None) -> str:
        # 黑字紫红底
        return cls.handle(message, "30", "45", "5")

    @classmethod
    def critical(cls, message: str = None) -> str:
        # 黑字红底
        return cls.handle(message, "30", "41", "5")


if __name__ == "__main__":
    # message_color = MessageColor()
    print(MessageColor.debug("debug"))
    print(MessageColor.info("info"))
    print(MessageColor.warn("warn"))
    print(MessageColor.error("error"))
    print(MessageColor.critical("critical"))
