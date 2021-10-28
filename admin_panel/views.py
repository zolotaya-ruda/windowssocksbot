from django.shortcuts import HttpResponse, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login


class AdminPanel:

    def get_login_page(self, request):
        return render(request, 'main/login.html')

    def get_main_page(self, request):
        return render(request, 'main/main.html')


class Handlers:

    def login_handler(self, request):

        username = request.POST['login']
        usr = User.objects.get(username=username)

        if usr.check_password(request.POST['password']):
            login(request, usr)
            return JsonResponse({'verdict': '200'})
        return HttpResponse('')
