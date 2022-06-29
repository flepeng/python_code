# 目录结构

- baiduyunpan_session：基于session 的百度云盘脚本
- baiduyunpan_OAuth2.0：基于 OAuth2.0 的百度云盘脚本
- config.ini: OAuth2.0 脚本的配置文件


# baiduyunpan_session

基于 session 的百度云盘脚本

参考连接
- https://zhuanlan.zhihu.com/p/109464640

主要实现了如下功能：

- 获取登录Cookie有效性；
- 获取网盘中指定目录的文件列表；
- 获取加密分享链接的提取码（对于没有提取码的链接也可以转存）；
- 转存分享的资源；
- 重命名网盘中指定的文件；
- 删除网盘中的指定文件；
- 移动网盘中指定文件至指定目录；
- 创建分享链接；

使用提示：

1. 使用前请在__init__方法中配置自己的登录cookie，配置好后可调用verifyCookie方法进行验证cookie的有效性！

2. 导入的Image，BytesIO，pytesseract这几个模块，是为了解决验证码，但是实际上使用的时候根本没有验证码，所以不想安装的可以屏蔽掉那一段；


# baiduyunpan_OAuth2.0

百度云网盘分享链接文件转存（基于OAuth2.0）

基于OAuth2.0，接口很稳定，不必担心web接口经常发生变化，也无需担心输入验证码、cookie过期等问题。


- 百度网盘开放平台地址：https://pan.baidu.com/union/doc/
- 参考git
    - https://github.com/iyzyi/BaiduYunTransfer
    - https://github.com/hxz393/BaiduPanFilesTransfers
    - https://github.com/Jljqbd/baidupan/blob/b5f24cd238a807f7f0e2095e6ac03f7fa7a26a90/BaiduPan.py


## 如何使用

| key        | value                       |
| ---------- | --------------------------- |
| api_key    | 应用id                      |
| secret_key | 应用secret                  |
| share_link | 分享链接                    |
| password   | 分享链接的提取码，长度为4位 |
| dir        | 转存路径，根路径为/         |

api_key和secret_key可以直接使用我程序里写好的，但是出于安全和QPS的考量，我推荐你自己再去申请一个，可以参考<https://pan.baidu.com/union/document/entrance#%E7%AE%80%E4%BB%8B>。

修改好以上几项后直接运行，第一次运行时需要你按照程序提示对应用进行授权。

## 注意

需要注意一点，由于受到权限的限制（程序仅拥有在/apps目录下的写入权限），程序无法帮你自动创建文件夹，需要你自己提前将转存路径的文件夹创建好。