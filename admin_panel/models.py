from django.db import models


class Bot(models.Model):
    ip = models.CharField(max_length=100, default='')

    uid = models.CharField(max_length=100)
    computername = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    is_win7 = models.BooleanField(default=False)
    is_winxp = models.BooleanField(default=False)
    is_win8 = models.BooleanField(default=False)
    is_win10 = models.BooleanField(default=False)
    is_win11 = models.BooleanField(default=False)

    is_online = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_x64 = models.BooleanField(default=False)
    is_server = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)
    date_ch = models.DateTimeField(auto_now=True)

    c = models.CharField(max_length=1, default='1')

    country = models.CharField(max_length=10)

    objects = models.Manager()

    class Meta:
        ordering = ['-date']


class Session(models.Model):
    uid = models.CharField(max_length=100)
    ip_port = models.CharField(max_length=50)
    connection_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
