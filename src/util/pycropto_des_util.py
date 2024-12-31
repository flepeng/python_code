from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from binascii import b2a_hex, a2b_hex


class DESUtil(object):
    def __init__(self, key: bytes):
        self.key = key  # 密钥key 长度必须为 16 位 128 bit（AES-128）、24（AES-192）、或 32（AES-256）Bytes 长度
        self.mode = DES.MODE_ECB
        self.cryptor = DES.new(self.key, self.mode)

    def encrypt(self, text: bytes) -> bytes:
        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        text = pad(text, DES.block_size)
        # 把拼接后的 16 位字符后传入加密类中，结果为字节类型
        encrypt_text = self.cryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(encrypt_text)

    def decrypt(self, text: bytes) -> bytes:
        decrypt_text = self.cryptor.decrypt(a2b_hex(text))
        return unpad(decrypt_text, DES.block_size)


def test_des():
    print("\n")
    key = b'abcdefgh'  # 密钥 8位或16位,必须为bytes
    obj = DESUtil(key)
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
    test_des()
