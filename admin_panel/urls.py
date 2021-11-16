from django.urls import path
from .views import AdminPanel, Handlers, Subsidiary
from django.conf import settings
from django.conf.urls.static import static

sub = Subsidiary()
ap = AdminPanel(sub)
handlers = Handlers(sub)

urlpatterns = [
    path('login/', ap.get_login_page, name='login_page'),
    path('login-handler/', handlers.login_handler, name='login_handler'),
    path('', ap.get_main_page, name='main_page'),
    path('gate/', handlers.gate, name='gate'),
    path('table/', ap.get_table_page, name='table_page'),
    path('ban/', handlers.ban, name='ban'),
    path('gate/backconnect/', handlers.back_connect, name='back_connect'),
    path('task/', ap.task, name='task'),
    path('admin-panel/', ap.admin_table, name='admin_table'),
    path('test/', handlers.test, name='test')
]
