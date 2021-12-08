import requests

import bot_pb2
import struct
from io import StringIO

bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = 'itsserv1'.encode('utf-16-le')
bot.computername = '12dczczc3'.encode('utf-16-le')
bot.username = '1232czc3'.encode('utf-16-le')
bot.os_major = 10
bot.os_minor = 0
bot.is_x64 = True
bot.is_server = True

r = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())
print(r.content.strip())


_r = bot_pb2.PanelMsg.RegistrationResult()
_r.ParseFromString(r.content.strip())
print(_r)

ar = bot_pb2.BotMsg.ActivityReport()
ar.uid = 'itsserv1'.encode('utf-16-le')

r1 = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
b = bot_pb2.PanelMsg.TaskGiveaway()
b.ParseFromString(r1.content.strip())
print(b.is_empty, b.task.task_id.decode('utf-16-le'), b.task.server, b.task.port, 'activ rep')
