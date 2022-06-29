# -*- coding:utf-8 -*-
"""
    @Time  : 2022/3/29  11:30
    @Author: Feng Lepeng
    @File  : compressed_files.py
    @Desc  :
"""
import os
import platform


WinRAR_exe_path = """C:\"Program Files"\\WinRAR\\WinRAR.exe a -p123 C:\\test.rar C:\\test.txt
"""


def compressed(rar_path, compressed_path, password):
    """
    加密压缩
    调用压缩成ZIP的CMD命令同RAR，只是输出路径不同，需将后缀改为.zip
    :param rar_path: 压缩文件的输出路径及其压缩的文件名，可以是 .rar or .zip
    :param compressed_path: 为需要压缩的文件路径
    :param password: 密码
    :return:
    """
    # 参数a表示添加压缩
    if platform == "Windows":
        cmd = WinRAR_exe_path + f" a -p{password} {rar_path} {compressed_path}"
    elif platform == "Linux":
        if password:
            cmd = f"zip -q -r -P {password} {rar_path} {compressed_path}"
        else:
            # cmd = f"tar –cvf  {rar_path} {compressed_path}"
            cmd = f"zip -re {rar_path} {compressed_path}"
    os.system(cmd)


if __name__ == '__main__':
    pass

