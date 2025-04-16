from app.controllers.authController import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginController.as_view(), name='auth-login'),
]