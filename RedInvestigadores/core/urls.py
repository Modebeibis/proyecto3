from django.urls import include, path, url
from django.contrib import admin

from django.contrib.auth import views
from . import forms

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.about_of, name='about_of'),
    path('', views.research, name='research'),
    path('', views.search_view, name='search_view'),
    path('', views.list_profiles, name='list_profiles'),
    path('', views.profile, name='profile'),
    path('', views.sedes, name='sedes'),
]
