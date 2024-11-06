from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt(data,simple_key):
    data = data.encode()
    cipher = AES.new(simple_key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = cipher.iv
    return iv + ct_bytes

def decrypt(iv_and_ct, simple_key):
    iv = iv_and_ct[:AES.block_size]   # Extract IV from the beginning
    ct = iv_and_ct[AES.block_size:]   # Ciphertext follows IV
    cipher = AES.new(simple_key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)  # Unpad the plaintext
    return pt.decode()


def generate_key(password):
    salt = get_random_bytes(32)
    return PBKDF2(password, salt, dkLen=32)

def do_encrypt(message,password):
    simple_key = generate_key(password)
    return encrypt(message,simple_key),simple_key

if __name__ == '__main__':

    data = 'hello world 1234'
    password = "ExamsAreCool"
    encrypted,key = do_encrypt(data,password)
    print(encrypted,end="\n\n")
    decrypted = decrypt(encrypted,key)
    print(decrypted)
