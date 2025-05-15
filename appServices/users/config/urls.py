"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.controllers.profilesController import *
from app.controllers.favoritesController import *
import uuid

urlpatterns = [
    path('admin/', admin.site.urls),
    path('artist/<str:id>', GetProfile.as_view(), name="findArtist"),
    path('profiles', GetProfile.as_view(), name="filterByNameOrBirthDate"),
    path('profile', GetProfile.as_view(), name="viewProfile"),
    path('profile/update', UpdateProfile.as_view(), name="updateProfile"),
    path('profile/delete', DeleteProfile.as_view(), name="deleteProfile"),

    path('favorites', GetFavorites.as_view(), name='get_favorites'),
    path('favorite/create', CreateFavorite.as_view(), name='create_favorite'),
    path('favorite/delete', DeleteFavorite.as_view(), name='delete_favorite'),
    path('favorite/<str:id>', GetFavorites.as_view(), name='get_favorite_by_id'),
]
