from app.controllers.authController import *
from app.controllers.accountsController import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin', admin.site.urls),
    path('login', LoginController.as_view(), name='authLogin'),
    path('register', RegisterController.as_view(), name='authRegister'),
    path('csrf', GetCsrfToken.as_view(), name="authGetCsrf"),
    path('refresh-token', RefreshToken.as_view(), name="authRefreshToken"),
    path('account/find', GetAccount.as_view(), name="accountGet"),
    path('account/update', UpdateAccount.as_view(), name="accountUpdate"),
    path('account/delete', DeleteAccount.as_view(), name="accountDelete") 
]