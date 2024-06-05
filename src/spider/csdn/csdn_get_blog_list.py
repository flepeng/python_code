# -*- coding:utf-8 -*-
"""
    @Author : Feng Lepeng
    @Date   : 2023/4/7 16:12
    @File   : csdn_get_blog_list.py
    @Desc   :
"""
from bs4 import BeautifulSoup


def main():
    with open("11.html", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, features="lxml")
    items = soup.find_all(name="article")
    sql_lists = []

    for i in items:
        url = i.find(name="a").get("href").replace("https://", "http://")
        view_num = i.find(class_="view-num").text.split()[0]
        title = i.find(name="h4").text
        sql_lists.append((url, view_num, title))

    print(sql_lists)
    sql_lists = sorted(sql_lists, key=lambda a: a[2])
    print(sql_lists)


if __name__ == '__main__':
    main()
