import requests
import bot_pb2

#bot = bot_pb2.BotMsg.RegisterBot()
#bot.uid = '123'.encode('utf-16-le')
#bot.computername = 'name'.encode('utf-16-le')
#bot.username = 'user'.encode('utf-16-le')
#bot.os_major = 10
#bot.os_minor = 0
#bot.is_x64 = True
#bot.is_server = True
#print(bot.SerializeToString())
r = requests.post(url='http://213.183.51.129:8002/test1/')
print(r.text)