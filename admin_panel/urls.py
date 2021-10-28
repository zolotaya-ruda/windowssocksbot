from django.urls import path, include
from .views import AdminPanel, Handlers

ap = AdminPanel()
handlers = Handlers()

urlpatterns = [
    path('login/', ap.get_login_page, name='login_page'),
    path('login-handler/', handlers.login_handler, name='login_handler'),
    path('', ap.get_main_page, name='main_page')
]