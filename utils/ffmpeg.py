# -*- coding:utf-8 -*-
"""
    @Time  : 2022/2/22  14:39
    @Author: Feng Lepeng
    @File  : ffmpeg.py
    @Desc  :
"""
import os
import platform
import logging

logger = logging.getLogger()
# ffmpeg windows 路径
ffmpeg_path = "C:\\Users\\Administrator\\Downloads\\ffmpeg-2022-01-17-git-dcc9454ab9-essentials_build\\bin\\ffmpeg.exe"


def merge_m3u8(m3u8_file, name, base_dir):
    """
    使用ffmpeg, 合并 m3u8 类视屏
    :param m3u8_file:
    :param name:
    :param base_dir:
    :return:
    """
    try:
        if platform == "Windows":
            cmd_ffmpeg_cut = ffmpeg_path + """ -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -ss 00:00:00.012 -c copy "{}" """
        elif platform == "Linux":
            cmd_ffmpeg_cut = """ffmpeg -allowed_extensions ALL -protocol_whitelist "file,http,crypto,tcp" -i "{}" -ss 00:00:00.012 -c copy "{}" """
        else:
            raise Exception("未知系统")

        out_path = '{}/{}.mp4'.format(base_dir, name)
        cmd = cmd_ffmpeg_cut.format(m3u8_file, out_path)
        logger.info(cmd)
        os.system(cmd)
        logger.info('视频合并完成')
    except Exception:
        logger.exception("合并失败")


if __name__ == '__main__':
    pass
