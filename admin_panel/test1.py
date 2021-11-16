import struct

import requests

import bot_pb2

session = bot_pb2.BackConnectMsg.NewConnection()

session.uid = '666'.encode('utf-16-le')
session.type = 1
session.port = 1

r = requests.post(url='http://127.0.0.1:8000/gate/backconnect/', data=struct.pack('=I', 1) + session.SerializeToString())
print(r.text)