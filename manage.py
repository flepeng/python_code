# -*- coding:utf-8 -*-

import os
import sys
import time
import urllib
import threading
import pymysql
import logging
import configparser


ffmpeg = "C:\\Users\\Administrator\\Downloads\\ffmpeg-2022-01-17-git-dcc9454ab9-essentials_build\\bin\\ffmpeg.exe"
zip = """C:\\"Program Files"\\WinRAR\\WinRAR.exe"""
cmd_ffmpeg = ffmpeg + """
 -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -c copy "{}"
"""
cmd_ffmpeg_cut = ffmpeg + """
 -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -ss 00:00:00.012 -c copy "{}"
"""
THREADS = 10
threads = []


def alter(file, old_str, new_str):
    """
    将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
    :param file: 文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)


def zip_encrypt(old_file_name, new_file_name, passwd="Pass"):
    """
    zip and 加密
    :param old_file_name: 01_今日内容.mp4
    :param new_file_name: 01.rar
    :param passwd:
    :return:
    """
    cmd = zip + " a -p{} {} {}".format(passwd, new_file_name, old_file_name)
    os.system(cmd)


def zip_encrypt_m3u8(old_file_name, old_file_path, new_file_name, passwd="Pass"):
    """
    zip and 加密
    :param old_file_name: 01_今日内容.mp4
    :param new_file_name: 01.rar
    :param passwd:
    :return:
    """
    cmd = zip + """ a -p{} "{}" "{}" "{}"
    """.format(passwd, new_file_name, old_file_name, old_file_path)
    print(cmd)
    os.system(cmd)


def exec_ffmpeg(file_name, new_video_path):
    """
    生成视频
    :param file_name:
    :param new_video_path:
    :return:
    """
    cmd = cmd_ffmpeg_cut.format(file_name, new_video_path)
    os.system(cmd)


def main():
    for root, dirs, files in os.walk("."):
        for file_name in files:
            base_name, ext_name = os.path.splitext(file_name)
            m3u8_path = "{}_contents".format(file_name)
            if ext_name == ".m3u8":
                alter(file_name, "file:///storage/emulated/0/UCDownloads/VideoData/", "")
                new_video_path = "../video/{}_1.mp4".format(base_name)
                new_video_zip_path = "../rar/{}.rar".format(base_name)
                new_video_zip_m3u8_path = "../rar_m3u8/{}_m3u8.rar".format(base_name)
                exec_ffmpeg(file_name, new_video_path)
                time.sleep(2)
                zip_encrypt(new_video_path, new_video_zip_path)
                zip_encrypt_m3u8(file_name, m3u8_path, new_video_zip_m3u8_path)


if __name__ == "__main__":
    main()

