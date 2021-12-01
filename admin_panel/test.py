import requests
import bot_pb2
import struct
from io import StringIO

bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = '5555'.encode('utf-16-le')
bot.computername = '12dczczc3'.encode('utf-16-le')
bot.username = '1232czc3'.encode('utf-16-le')
bot.os_major = 6
bot.os_minor = 2
bot.is_x64 = True
bot.is_server = False
#r = requests.post(url='http://185.250.151.137:80/gate/', data='1'.encode('utf-8'))
#r = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())

#print(r.text, 'text')
#_r = bot_pb2.PanelMsg.RegistrationResult()
#_r.ParseFromString(r.content)
#print(_r)


ar = bot_pb2.BotMsg.ActivityReport()
ar.uid = '1234'.encode('utf-16-le')

r1 = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
b = bot_pb2.PanelMsg.TaskGiveaway()
b.ParseFromString(r1.content)
print(b.is_empty, b.task.task_id.decode('utf-16-le'), b.task.server, b.task.port, 'activ rep')

task = bot_pb2.BotMsg.TaskCompleted()
task.task_id = '34'.encode('utf-16-le')
task.result = True
task.uid = '1234'.encode('utf-16-le')

r2 = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 3) + task.SerializeToString())
print(r2.text)