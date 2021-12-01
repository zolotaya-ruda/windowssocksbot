from django.contrib import admin
from .models import Bot, Session, Task, IPBackConnect

admin.site.register(Bot)
admin.site.register(Session)
admin.site.register(Task)
admin.site.register(IPBackConnect)

# Register your models here.
