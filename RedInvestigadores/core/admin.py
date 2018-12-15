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

class AuthorOfAdmin(admin.ModelAdmin):
    fields = ['publication', 'person']
    list_display = ('publication', 'person')

class GrantParticipantAdmin(admin.ModelAdmin):
    fields = ['grant', 'person']
    list_display = ('grant', 'person')

class GroupMemberAdmin(admin.ModelAdmin):
    fields = ['group', 'person']
    list_display = ('group', 'person')

class StudentOfAdmin(admin.ModelAdmin):
    fields = ['tutor', 'student']
    list_display = ('tutor', 'student')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Administrator)
admin.site.register(Affiliation)
admin.site.register(AuthorOf, AuthorOfAdmin)
admin.site.register(Grant)
admin.site.register(GrantParticipant, GrantParticipantAdmin)
admin.site.register(Group)
admin.site.register(GroupMember, GroupMemberAdmin)
admin.site.register(Journal)
admin.site.register(Person)
admin.site.register(PersonRole)
admin.site.register(Postdoc)
admin.site.register(Publication)
admin.site.register(Researcher)
admin.site.register(Student)
admin.site.register(StudentOf, StudentOfAdmin)
