# free_proxy

一个收集 提供免费代理网站的代理的 工具 

## 运行

- 源码下载:

  ```
  https://github.com/flepeng/free_proxy.git
  ```

- 安装依赖:

  ```
  pip install -r requirements.txt
  ```
  
- 运行

  ```
  python src/spider/spiders.py
  ```

- 配置
  
  src/spider/spiders.py 文件中的每个类分别代表一个不同的提供免费代理的网站爬虫，想运行哪个爬虫就实例化该爬虫


# 代理网址

## 已收集的代理[只收集免费的]

- 快代理
    - [收费的](https://www.kuaidaili.com/)
    - [免费的高匿](https://www.kuaidaili.com/free/inha), ☆
    - [免费的透明](https://www.kuaidaili.com/free/intr), ☆
    - [免费高速HTTP代理IP列表](https://www.kuaidaili.com/ops/proxylist/), ☆

- 米扑代理
    - [收费的](https://proxy.mimvp.com/)
    - [免费的](https://proxy.mimvp.com/freesecret) ★：免费的代理只能看10个，而且是从晚上扫描来的
    
- 开心代理
    - [收费的](http://www.kxdaili.com/)
    - [免费的](http://www.kxdaili.com/dailiip/1/1.html)★：免费代理是通过网络扫描得来

- 蝶鸟IP
    - [收费的](https://www.dieniao.com/)
    - [免费的](https://www.dieniao.com/FreeProxy/1.html)★
 
- 66IP代理
    - [收费的](http://www.66daili.cn/)
    - [免费的](http://www.66ip.cn) ★★
   
- 云代理IP
    - [免费的高匿](http://www.ip3366.net/free/?stype=1)★
    - [免费的透明 or 普匿](http://www.ip3366.net/free/?stype=2')★

- 小幻代理
    - [免费的](https://ip.ihuan.me/)★★:代理地址很多

- 89免费代理 
    - [免费的](https://www.89ip.cn/)☆

- 免费代理IP
    - [免费的](http://ip.jiangxianli.com/)☆

- 无忧代理
    - [收费的](https://www.data5u.com/)

- free proxy
    - [免费的](https://www.freeproxylists.net/zh/) 有人机校验，爬虫不好爬

## 无效的代理

- 全网IP代理
    - http://www.goubanjia.com          
- 西刺IP代理
    - https://www.xicidaili.com/nn      高匿
    - https://www.xicidaili.com/nt      透明
- IP海代理
    - 'http://www.iphai.com/free/ng',  # 国内高匿
    - 'http://www.iphai.com/free/np',  # 国内普通
    - 'http://www.iphai.com/free/wg',  # 国外高匿
    - 'http://www.iphai.com/free/wp',  # 国外普通

- http://www.youdaili.net/Daili/http/
- http://gatherproxy.com/
- http://www.ip181.com/
- https://hidemy.name/en/proxy-list

- 3464
    - http://www.3464.com/data/Proxy/http/
- coderbusy
    - https://proxy.coderbusy.com/
- 万能代理
    - http://wndaili.cn/


## 未收集的代理

- coolproxy
    - https://www.cool-proxy.net/proxies/http_proxy_list/country_code:/port:/anonymous:/page:2
- proxy11
    - https://proxy11.com/free-proxy/anonymous
- proxy list
    - https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
- proxydb
    - http://proxydb.net/


# 代理ip素材库

不确定是否有效

- https://raw.githubusercontent.com/a2u/free-proxy-list/master/free-proxy-list.txt


# github 项目

## 直接运行的

### fetch-some-proxies 可用

项目地址： https://github.com/stamparm/fetch-some-proxies

- 现获取一个代理ip 的 txt 文件
- 然后循环该文件，判断里面的ip 哪些可用

注意：获取的 proxy 可能有重复的，不同的线程可能在同一时间拿到该 proxy，都去查询数据库，但是无记录，所以都去判断该 proxy 是否可用，如果可用，则同时存入数据库，导致数据重复。


## 其他项目已包含该项目的所有代理地址，不需要重复运行的

### ProxyPool 

git 地址：https://github.com/yyyy777/ProxyPool

ProxyPool/crawlProxy/crawlProxy.py 文件 getProxySecond 可用

该项目中所有的代理地址已经收录

### https://github.com/Karmenzind/fp-server (22 Mar 2019)

该项目中所有的代理地址已经收录

### https://github.com/jhao104/proxy_pool

该项目中所有的代理地址已经收录

### https://github.com/qiyeboy/IPProxyPool (25 Dec 2017)

该项目中所有的代理地址已经收录

### https://github.com/cwjokaka/ok_ip_proxy_pool (10 May 2020)

该项目中所有的代理地址已经收录

### https://github.com/awolfly9/IPProxyTool (on 10 Mar 2021)

该项目中所有的代理地址已经收录


## 未验证的项目

### https://github.com/rootVIII/proxy_requests

好像要安装库能直接获取代理的地址，没有试。

### https://github.com/Ge0rg3/requests-ip-rotator

使用 aws 的代理

### https://github.com/JaredLGillespie/proxyscrape

后续要搞的项目2


# 爬虫评测

https://zhuanlan.zhihu.com/p/33576641



