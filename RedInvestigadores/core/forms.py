from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import *
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
import re

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label  = 'Ingresa tu contraseña'
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder':'Contraseña'})
        self.fields['login'].label     = 'Escribe tu correo'
        self.fields['login'].widget    = forms.TextInput(attrs={'placeholder':'Correo electrónico'})

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='Nombres')
    last_name  = forms.CharField(max_length=30, label='Apellidos')
    email      = forms.EmailField(label='Correo Electrónico')
#    state      = forms.ModelChoiceField(queryset=State.objects.all(), label='Estado')

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        user.save()
        return user

    def clean_name(self,cd):
        first_name = cd.get("first_name")
        last_name = cd.get("last_name")
        bad_firstName = bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', first_name))
        bad_lastName = bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', last_name))
        if not(bad_firstName) or not(bad_lastName):
            raise forms.ValidationError("Nombre(s) o Apellidos invalidos, " +
                                                "intenta no usar números ó cáracteres especiales")
        return cd
    
    def clean_password(self,cd):
        password = cd.get("password1")
        if len(str(password)) <= 4:
            raise forms.ValidationError("Contraseña invalida, intenta usar una contraseña "+
                                                "mayor a 4 caráteres.")
        return cd

    def clean(self):
        cd = self.cleaned_data
        cd = self.clean_name(cd)
        cd = self.clean_password(cd)
        return cd


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
        self.fields['username'].label  = 'Usuario'
#        self.fields['email'].label     = 'Correo Electrónico'
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
        self.fields['username'].label   = "Usuario"
        self.fields['first_name'].label = "Nombres"
        self.fields['last_name'].label  = "Apellidos"
        self.fields['email'].label      = "Correo electrónico"

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


class ProfileForm(forms.ModelForm):
    orcid = forms.CharField(label='ORCID')
    class Meta:
        model=Person
        fields=('first_name','last_name','affiliation','state','degree','sni')
        labels = {
            'first_name' : _('Nombres'),
            'last_name'  : _('Apellidos'),
            'affiliation': _('Sede'),
            'state'      : _('Estado'),
            'degree'     : _('Título'),
            'sni'        : _('SNI')
        }
    
    def clean_name(self,cd):
        first_name = cd.get("first_name")
        last_name = cd.get("last_name")
        bad_firstName = bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', first_name))
        bad_lastName = bool(re.fullmatch('[A-Za-z]{2,25}( [A-Za-z]{2,25})?', last_name))
        if not(bad_firstName) or not(bad_lastName):
            raise forms.ValidationError("Nombre(s) o Apellidos invalidos, " +
                                                "intenta no usar números ó cáracteres especiales")
        return cd
    
    def clean(self):
        super().clean()
        cd = self.cleaned_data
        cd = self.clean_name(cd)
        return cd

    def __init__(self,*args, **kwargs):
        super(ProfileForm, self).__init__(*args,**kwargs)
        self.fields['affiliation'].queryset = Affiliation.objects.all()
        self.fields['state'].queryset = State.objects.all()
        self.fields['degree'].queryset = Person.DEGREE_CHOICES
        self.fields['sni'].queryset = Person.SNI_CHOICES

class PublicationPetitionForm(forms.Form):
    years = []
    for i in range (0, 90):
        years.append(1940+i)
    title     = forms.CharField(label = 'Título', max_length = 200)
    journal   = forms.ChoiceField(label = 'Revista')
    volume    = forms.IntegerField(label = 'Volumen',min_value=1)
    issue     = forms.IntegerField(label = 'Número',min_value=0)
    date      = forms.DateField(widget = forms.SelectDateWidget(years=years),
                                label = 'Fecha publicación')
    doi       = forms.CharField(label = 'DOI')
    authors   = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          label ='Autores')

    def __init__(self, *args, **kwargs):
        super(PublicationPetitionForm, self).__init__(*args, **kwargs)
        J_CHOICES = ((journal.id, journal.__str__()) for journal in Journal.objects.all())
        self.fields['journal'].choices = J_CHOICES
        OPTIONS   = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['authors'].choices = OPTIONS

class PublicationChangeForm(forms.ModelForm):
    doi       = forms.CharField(label = 'DOI')
    title     = forms.CharField(label = 'Título', max_length = 200)
    authors   = forms.MultipleChoiceField(label= 'autores', widget=forms.CheckboxSelectMultiple)

    class Meta:
        model=Publication
        fields=('journal', 'volume','issue','date')
        labels = {
            'journal': _('Revista'),
            'volume' : _('Volumen'),
            'issue' : _('Número'),
            'date' : _('Fecha'),
        }
    def __init__(self,*args, **kwargs):
        super(PublicationChangeForm, self).__init__(*args, **kwargs)
        self.fields['journal'].queryset = Journal.objects.all()
        OPTIONS   = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['authors'].choices = OPTIONS


class GroupPetitionForm(forms.Form):
    name = forms.CharField(label = 'Nombre', max_length = 200)
    members = forms.MultipleChoiceField(label= 'Miembros',widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(GroupPetitionForm, self).__init__(*args, **kwargs)
        OPTIONS = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['members'].choices = OPTIONS
