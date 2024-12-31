import rsa
from rsa.key import PublicKey, PrivateKey
from binascii import b2a_hex, a2b_hex


class RSAUtil(object):
    def __init__(self, pub_key: PublicKey, pri_key: PrivateKey):
        self.pub_key = pub_key
        self.pri_key = pri_key

    def generate(self):
        # 生成RSA密钥对
        self.pub_key, self.pri_key = rsa.newkeys(2048)

    def save_key(self, pri_file="privkey.pem", pub_file="pubkey.pem"):
        pub = self.pub_key.save_pkcs1()
        pri = self.pri_key.save_pkcs1('PEM')  # save_pkcsl()是内置方法，其默认参数是‘PEM'
        with open(pub_file, mode='wb') as f, open(pri_file, mode='wb') as f1:
            f.write(pub)  # 打开两个文件，分别存储公钥及私钥
            f1.write(pri)

    def load_key(self, pri_file="privkey.pem", pub_file="pubkey.pem"):
        with open(pub_file, mode='rb') as f, open(pri_file, 'rb') as f1:
            pub = f.read()  # 从文件中再读出公钥和私钥
            pri = f1.read()
            self.pub_key = rsa.PublicKey.load_pkcs1(pub)   # 转换为原始状态
            self.pri_key = rsa.PrivateKey.load_pkcs1(pri)

    def encrypt(self, text: bytes) -> bytes:
        cipher_text = rsa.encrypt(text, self.pub_key)
        # 因为 RSA 加密得到的字符串是二进制的，不一定是 ascii 字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(cipher_text)

    def decrypt(self, text: bytes) -> bytes:
        decrypt_text = rsa.decrypt(a2b_hex(text), self.pri_key)
        return decrypt_text


def test_rsa():
    pub_key, pri_key = rsa.newkeys(2048)
    obj = RSAUtil(pub_key, pri_key)
    for i in ["2222sdf", "中国", "撒娇的福利卡就来反馈阿斯利康都放假啦数据的立法"]:
        text = i.encode()
        encrypt_text = obj.encrypt(text)
        decrypt_text = obj.decrypt(encrypt_text)
        print("原数据", text)
        print("加密之后的数据", encrypt_text.decode())
        print("解密之后的数据", decrypt_text.decode())
        print("==============")


if __name__ == '__main__':
    test_rsa()
