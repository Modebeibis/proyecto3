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
from django.urls import path,re_path, include
from core import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from core.forms import LoginForm, CustomUserCreationForm

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name='registration/login.html',
        authentication_form=LoginForm), name='login'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('home/', views.home, name='home'),
    path('profile/<int:user_id>', views.get_user_profile, name='profile'),
    path('research/',views.profile_changes, name='research'),
    path('about_of/', views.about_of, name='about_of'),
    path('search_view/', views.search_view, name='search_view'),
    path('search_view/search', views.search, name='search'),
    path('signup/', views.signup, name='signup'),
    path('signup/core/account_activation_sent/',views.account_activation_sent, name='account_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.activate, name='activate'),
    path('sedes/', views.get_affiliations, name='sedes'),
    path('sedes/<int:affiliation_id>', views.get_affiliation, name='sede'),
    path('estados/<int:state_id>', views.get_state_info, name='estado'),
    path('publicacion/<int:publication_id>', views.get_publication, name='publication'),
    path('grupo/<int:group_id>', views.get_group, name='group'),
    path('actualizar/grupo/<int:group_id>',views.group_changes, name='group_change'),
    path('proyecto/<int:grant_id>', views.get_grant, name='grant'),
    path('crear/articulo', views.get_publication_petition, name='publication_petition'),
    path('crear/grupo', views.get_group_petition, name='group_petition'),
    path('crear/proyecto', views.get_grant_petition, name='grant_petition'),
    path('crear/sede', views.get_affiliation_petition, name='affiliation_petition'),
    path('actualizar/publicacion/<int:publication_id>', views.publication_changes, name='publication_change'),
    path('', include('django.contrib.auth.urls')),
    path('', views.home, name='home'),
]
