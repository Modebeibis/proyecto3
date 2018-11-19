from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm

from .models import *

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username']

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Administrator)
admin.site.register(Affiliation)
admin.site.register(Grant)
admin.site.register(Group)
admin.site.register(ExternalAuthor)
admin.site.register(Journal)
admin.site.register(Person)
admin.site.register(Postdoc)
admin.site.register(Publication)
admin.site.register(Researcher)
admin.site.register(Role)
admin.site.register(Student)
