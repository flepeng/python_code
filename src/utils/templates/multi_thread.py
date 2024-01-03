# -*- coding:utf-8 -*-
"""
    @Time  : 2022/4/2  18:08
    @Author: Feng Lepeng
    @File  : multi_thread.py
    @Desc  :
"""
import os
import sys
import time
import threading

if sys.version_info >= (3, 0):
    import queue
    Queue = queue.Queue
    xrange = range
else:
    import Queue
    Queue = Queue.Queue


THREADS = 10
threads = []


def work(queue):
    try:
        while True:
            info = queue.get_nowait()

    except Exception as e:
        return
        # logging.exception("")


def multi_thread(info_list):
    if len(info_list) == 0:
        print("[!] no info found")
        return

    queue = Queue()
    for info in info_list:
        queue.put(info)

    for _ in xrange(THREADS):
        thread = threading.Thread(target=work, args=[queue, ])
        thread.daemon = True

        try:
            thread.start()
        except threading.ThreadError as ex:
            sys.stderr.write("[x] error occurred while starting new thread ('%s')" % ex.message)
            break

        threads.append(thread)

    try:
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.is_alive():
                    alive = True
                    time.sleep(0.1)
    except KeyboardInterrupt:
        sys.stderr.write("\r   \n[!] Ctrl-C pressed\n")
    else:
        sys.stdout.write("\n[i] done\n")
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(0)


if __name__ == '__main__':
    pass
