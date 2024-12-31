from binascii import a2b_hex, b2a_hex
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class RSAUtil(object):
    def __init__(self, pub_key, pri_key):
        self.pub_key = pub_key
        self.pri_key = pri_key

    def generate(self):
        # 生成RSA密钥对
        key = RSA.generate(2048)
        self.pri_key = key.export_key()
        self.pub_key = key.publickey().export_key()

    def save_key(self, pub_file="./id_rsa.pub", pri_file="./id_rsa"):
        # 可以使用public_key方法获取公钥
        with open(pub_file, "wb") as f, open(pri_file, "wb") as f1:
            f.write(self.pub_key)
            f1.write(self.pri_key)

    def load_key(self, pub_file="./id_rsa.pub", pri_file="./id_rsa"):
        # 可以使用public_key方法获取公钥
        with open(pub_file, "wb") as f, open(pri_file, "wb") as f1:
            self.pub_key = f.read()
            self.pri_key = f1.read()

    def encrypt(self, text: bytes) -> bytes:
        # 加密
        rsa_public_key = RSA.import_key(self.pub_key)
        rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
        cipher_text = rsa_public_key.encrypt(text)
        return b2a_hex(cipher_text)

    def decrypt(self, text: bytes) -> bytes:
        # 解密
        rsa_private_key = RSA.import_key(self.pri_key)
        rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
        decrypt_text = rsa_private_key.decrypt(a2b_hex(text))
        return decrypt_text


def test_rsa():
    print("\n")
    # 生成RSA密钥对
    key = RSA.generate(2048)
    pri_key = key.export_key()
    pub_key = key.publickey().export_key()
    obj = RSAUtil(pub_key, pri_key)
    for i in [
        "000000000",
        "中国",
        "sajfkljaslkfjflkasjflka",
        "啊接口两地分居阿莱克斯江东父老看见阿斯利康福建省开朗大方即可撒对江东父老看见阿斯利康的肌肤"]:
        text = i.encode()
        encrypt_text = obj.encrypt(text)
        decrypt_text = obj.decrypt(encrypt_text)
        print("原数据", i)
        print("加密之后的数据", encrypt_text.decode())
        print("解密之后的数据", decrypt_text.decode())
        print("==============")


if __name__ == '__main__':
    test_rsa()
