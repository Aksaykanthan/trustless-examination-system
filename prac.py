# import random
# import datetime
# print(random.randint(100000,200000))
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# startTime = datetime.datetime.now()
# endTime = startTime + datetime.timedelta(minutes=30)
# print(startTime)
# print(endTime)
# import json
# import random
# with open("data/QuestionPaper.json",'r') as f:
#     data = json.load(f)
#     print(random.choice(data))

# message = "hello world 1234"
# data = message.encode()
# salt = get_random_bytes(32)
# password = "Hello"
# simple_key = PBKDF2(password, salt, dkLen=32)
# print(simple_key)

