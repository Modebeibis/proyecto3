from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.log_in, name='log_in'),
    path('', views.about_of, name='about_of'),
    path('', views.research, name='research'),
    path('', views.search_view, name='search_view'),
]
