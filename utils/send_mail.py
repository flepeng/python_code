# -*- coding:utf-8 -*-
"""
    @Time  : 2022/2/25  20:14
    @Author: Feng Lepeng
    @File  :
    @Desc  : 发送邮件脚本
                1、因为 连接 smtp 服务器会花费较多时间，所以 本脚本不提供断开 smtp 功能
                2、所有的 SendMail 实例使用同一个 smtp 连接
"""
import os
import time
import smtplib
import platform

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from utils.logging import logger
from utils.op_ini import conf


class SendMail(object):
    smtp = ""
    smtp_server = "smtp.xxxxxx.com"
    smtp_port = 25
    smtp_sender = "flepeng@xxxxxx.com"
    smtp_sender_password = "xxxxxx"

    def __init__(
            self,
            smtp_receiver="",
            smtp_receiver_default=[],
            smtp_cc=[],
            smtp_subject="",
            smtp_appendix_list="",
            smtp_body="默认内容",
            body_image_list=""
    ):
        self.msg = None

        self.smtp_body = smtp_body  # 邮件内容
        self.body_image_list = body_image_list  # 邮件内容中包含图片的时候，图片的列表

        self.smtp_receiver = smtp_receiver  # 邮件接收人
        self.smtp_receiver_default = smtp_receiver_default  # 测试时默认的邮件接收人
        self.smtp_cc = smtp_cc  # 邮件抄送人
        self.smtp_subject = smtp_subject  # 邮件的主题
        self.smtp_appendix_list = smtp_appendix_list  # 邮件的附件

    @classmethod
    def __login(cls):
        start = time.time()
        try:
            cls.smtp = smtplib.SMTP(cls.smtp_server)
            cls.smtp.connect(cls.smtp_server, cls.smtp_port)
            cls.smtp.ehlo()  # 向邮箱发送 SMTP "ehlo" 命令
            cls.smtp.starttls()
            cls.smtp.login(user=cls.smtp_sender, password=cls.smtp_sender_password)
            logger.info("login success, spend time: {}".format(time.time()-start))
        except Exception:
            logger.exception("connect mail server fail")
            return

    def __is_connected(self):
        try:
            status = self.smtp.noop()[0]
        except Exception:  # smtplib.SMTPServerDisconnected
            logger.info("The mail session is invalid. Log in again")
            status = -1

        if status != 250:
            self.__login()

    def send_mail(self):
        self.__is_connected()

        try:
            self.mail_content()

            logger.info("=" * 50)
            logger.info("【发送邮件】接受人：{},抄送人：{}".format(self.smtp_receiver, self.smtp_cc))
            logger.info("【发送邮件】邮件主题：{},邮件内容：{}".format(self.smtp_subject, self.smtp_body))

            sysstr = platform.system()
            mail_flag = conf.MAIL

            if sysstr == "Windows" or not mail_flag:
                self.smtp_receiver = self.smtp_receiver_default
                self.smtp_cc = []
                logger.info("【发送邮件】实际接受人：{},抄送人：{}".format(self.smtp_receiver, self.smtp_cc))

            logger.info("=" * 50)

            self.smtp.sendmail(self.smtp_sender, self.smtp_receiver + self.smtp_cc, self.msg.as_string())

        except Exception:
            logger.exception("send mail fail")
        # finally:
        #     self.smtp.quit()

    def mail_content(self):
        self.msg = MIMEMultipart()
        self.msg.attach(MIMEText(self.smtp_body, "html", "utf-8"))
        self.msg["from"] = self.smtp_sender
        self.msg["to"] = ";".join(self.smtp_receiver)
        self.msg["Cc"] = ";".join(self.smtp_cc)
        self.msg["subject"] = self.smtp_subject

        if self.body_image_list:
            for i in self.body_image_list:
                self.msg.attach(i)

        if self.smtp_appendix_list:
            for i in self.smtp_appendix_list:
                attr = MIMEApplication(open(i, "rb").read())
                attr.add_header("Content-Disposition", "attachment", filename=os.path.split(i.encode("UTF-8"))[1])
                self.msg.attach(attr)


if __name__ == "__main__":
    obj = SendMail(smtp_body="222222222")
    obj.send_mail()
    time.sleep(10)
    obj = SendMail(smtp_body="1111111111")
    obj.send_mail()
