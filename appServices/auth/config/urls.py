from app.controllers.authController import *
from app.controllers.accountsController import *
from app.controllers.passwordResetController import *
from app.controllers.rolesController import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin', admin.site.urls),
    path('auth/login', LoginController.as_view(), name='authLogin'),
    path('auth/register', RegisterController.as_view(), name='authRegister'),
    path('auth/csrf', GetCsrfToken.as_view(), name="authGetCsrf"),
    path('auth/refresh-token', RefreshToken.as_view(), name="authRefreshToken"),
    path('account/find', GetAccount.as_view(), name="accountGet"),
    path('account/update', UpdateAccount.as_view(), name="accountUpdate"),
    path('account/delete', DeleteAccount.as_view(), name="accountDelete"),
    path('password-reset/request', RequestPasswordReset.as_view(), name='request-password-reset'),
    path('password-reset/verify', VerifyAndResetPassword.as_view(), name='verify-password-reset'),
    path('role/create', CreateRole.as_view(), name='create_role'),
    path('role/update', UpdateRole.as_view(), name='update_role'),
    path('role/delete', DeleteRole.as_view(), name='delete_role'),
    path('role/<str:id>', GetRoles.as_view(), name='get_role_by_id'),
    path('roles', GetRoles.as_view(), name='get_roles'),
]