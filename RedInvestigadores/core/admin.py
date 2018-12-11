from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import AdminSite

from .forms import LoginForm, CustomUserCreationForm, CustomUserChangeForm

from .models import *

admin.site.site_header = 'Administración del Sitio'

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']

class PersonAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'user', 'state']
    list_display = ('first_name', 'last_name', 'user', 'state')

class AdministratorAdmin(admin.ModelAdmin):
    fields = ['person',]
    list_display = ('person',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Administrator, AdministratorAdmin)
admin.site.register(Affiliation)
admin.site.register(Grant)
admin.site.register(Group)
admin.site.register(ExternalAuthor)
admin.site.register(Journal)
admin.site.register(Person, PersonAdmin)
admin.site.register(PersonRole)
admin.site.register(Postdoc)
admin.site.register(Publication)
admin.site.register(Researcher)
admin.site.register(Student)
