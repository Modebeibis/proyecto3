"""RedInvestigadores URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name = 'home'),
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('research/',views.research, name='research'),
    path('about_of/', views.about_of, name='about_of'),
    path('list_profiles/search_view/', views.search_view, name='search_view'),
    path('list_profiles/search_view/search', views.search, name='search'),
    path('list_profiles/', views.list_profiles, name='list_profiles'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('sedes/', views.sedes, name='sedes'),
    path('', include('django.contrib.auth.urls')),
]
