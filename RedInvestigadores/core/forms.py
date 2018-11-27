from django import forms
from django.contrib.auth.forms import  AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser
from django.utils.translation import ugettext_lazy as _

class LoginForm(AuthenticationForm):
    def __init__(self, request,*args, **kwargs):
        super().__init__(request,*args,**kwargs)
        self.fields['username'].label = 'Escribe tu usuario'
        self.fields['password'].label = 'Ingresa tu contraseña'

    class Meta(AuthenticationForm):
        model = CustomUser
        fields=('username','password')


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Usuario'
        self.fields['email'].label = 'Correo Electrónico'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirma tu contraseña'

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
          'username': forms.Textarea(attrs={'rows':1,
                                            'cols':60,
                                            'style':'resize:none;'}),
        }


class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = "Usuario"
        self.fields['first_name'].label = "Nombres"
        self.fields['last_name'].label = "Apellidos"
        self.fields['email'].label = "Correo electrónico"

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)
        widgets = {
          'username'  : forms.Textarea(attrs={'rows':1,
                                              'cols':33,
                                              'style':'resize:none;'}),
          'first_name': forms.Textarea(attrs={'rows':1,
                                              'cols':33,
                                              'style':'resize:none;'}),
          'last_name' : forms.Textarea(attrs={'rows':1,
                                              'cols':33,
                                              'style':'resize:none;'}),
        }

#class ProfileForm(forms.Form):
