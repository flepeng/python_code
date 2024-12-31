from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from binascii import b2a_hex, a2b_hex


class AESUtil(object):
    def __init__(self, key: int, mode: int = AES.MODE_ECB):
        self.key = key  # 密钥key 长度必须为 16 位 128 bit（AES-128）、24（AES-192）、或 32（AES-256）Bytes 长度
        if mode == AES.MODE_ECB:  # 加密模式。它应该是AES.MODE_XXX常量之一，如AES.MODE_ECB、AES.MODE_CBC 等
            self.encryptor = self.decryptor = AES.new(self.key, AES.MODE_ECB)
        elif mode == AES.MODE_CBC:
            self.encryptor = AES.new(self.key, AES.MODE_CBC, self.key)
            self.decryptor = AES.new(self.key, AES.MODE_CBC, self.key)  # 加密和解密不能用同一个
        else:
            raise KeyError("暂不支持")

    def generate(self):
        key = get_random_bytes(16)

    def encrypt(self, text):
        # 加密函数，如果text不是16的倍数【加密文本text必须为16的倍数！】，那就补足为16的倍数
        text = pad(text, AES.block_size)
        # 把拼接后的 16 位字符后传入加密类中，结果为字节类型
        encrypt_text = self.encryptor.encrypt(text)
        # 因为AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(encrypt_text)

    def decrypt(self, text):
        decrypt_text = self.decryptor.decrypt(a2b_hex(text))
        return unpad(decrypt_text, AES.block_size)


def test_aes():
    print("\n")
    obj = AESUtil(b'keyskeyskeyskeys', AES.MODE_ECB) # 密钥16位,必须为bytes
    # obj = AESUtil(b'keyskeyskeyskeys', AES.MODE_CBC) # 密钥16位,必须为bytes
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
    test_aes()
