from django.urls import path
from .views import AdminPanel, Handlers
from django.conf import settings
from django.conf.urls.static import static

ap = AdminPanel()
handlers = Handlers()

urlpatterns = [
    path('login/', ap.get_login_page, name='login_page'),
    path('login-handler/', handlers.login_handler, name='login_handler'),
    path('', ap.get_main_page, name='main_page'),
    #path('gate/')
]