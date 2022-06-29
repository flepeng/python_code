# -*- coding:utf-8 -*-

import os
import cv2 as cv


def cut_video(video_file):
    print(video_file)
    print(os.path.exists(video_file))
    # 导入视频文件，参数：0 自带摄像头，1 USB摄像头，为文件名时读取视频文件
    video_caputre = cv.VideoCapture(video_file)

    # 获取读入视频的参数
    fps = video_caputre.get(cv.CAP_PROP_FPS)
    width = video_caputre.get(cv.CAP_PROP_FRAME_WIDTH)
    height = video_caputre.get(cv.CAP_PROP_FRAME_HEIGHT)

    print("fps:", fps)
    print("width:", width)
    print("height:", height)

    # 定义截取尺寸,后面定义的每帧的h和w要于此一致，否则视频无法播放
    # 注意 这里是高宽 (height, width)
    size = (int(height), int(width))

    # 创建视频写入对象
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    # fourcc = cv.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video_write = cv.VideoWriter("01videoFrameTarget.avi", fourcc, fps, size)

    frame_skip = 1
    frame_now = 0
    # 读取视频帧，然后写入文件并在窗口显示
    success, frame_src = video_caputre.read()
    while success and not cv.waitKey(1) == 27:  # 读完退出或者按下 esc 退出
        frame_now += 1
        if frame_now <= frame_skip:
            continue
        # [width, height] 要与上面定义的size参数一致，注意参数的位置
        # frame_target = frame_src[0:int(width), 0:int(height)]
        frame_target = frame_src
        # 写入视频文件
        video_write.write(frame_target)

        # 显示裁剪的视频和原视频
        # cv.imshow("video", frame_target)
        # cv.imshow("Video_src", frame_src)

        # 不断读取
        success, frame_src = video_caputre.read()

    print("视频裁剪完成")

    # 销毁窗口，释放资源
    # cv.destroyWindow("video")
    # cv.destroyWindow("Video_src")
    video_caputre.release()
    video_write.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    video_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "01_今日内容.mp4")
    video_file = "01_今日内容.mp4"
    cut_video(video_file, "01.rar")