from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import *
from django.utils.translation import ugettext_lazy as _
from allauth.account.forms import LoginForm, SignupForm
import re

"""
Module that contains all the forms needed for the web page.
"""
class CustomLoginForm(LoginForm):
    """
    Form for the login.
    """
    def __init__(self, *args, **kwargs):
        """
        Initiates the form with a field for the password and one for
        the email.
        """
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label  = 'Ingresa tu contraseña'
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder':'Contraseña'})
        self.fields['login'].label     = 'Escribe tu correo'
        self.fields['login'].widget    = forms.TextInput(attrs={'placeholder':'Correo electrónico'})

class CustomSignupForm(SignupForm):
    """
    Form for the signup.
    It has three fields: first_name, last_name and email.
    The user needs to fill these three fiels in order to
    get succesfully registered.
    """
    first_name = forms.CharField(max_length=30, label='Nombres')
    last_name  = forms.CharField(max_length=30, label='Apellidos')
    email      = forms.EmailField(label='Correo Electrónico')

    def signup(self, request, user):
        """
        Cleans the data, saves it into the new user created and returns the user.
        """
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        user.save()
        return user

    def clean_name(self,cd):
        """
        Verifies that the user is not using strange characters into his first name and
        last name
        """
        first_name = cd.get("first_name")
        last_name = cd.get("last_name")
        correct_name = [name for name in [x.isalpha() for x
                                        in str(first_name).split(" ")] if not(name)]
        correct_last_name = [name for name in
                                [x.isalpha() for x in str(last_name).split(" ")] if not(name)]
        if len(correct_name) > 0 or len(correct_last_name) > 0:
            raise forms.ValidationError("Nombre(s) o Apellidos invalidos, " +
                                                "intenta no usar números ó cáracteres especiales")
        return cd

    def clean_password(self,cd):
        """Cleans the password and verifies that it is valid.
        """
        password = cd.get("password1")
        if len(str(password)) <= 4:
            raise forms.ValidationError("Contraseña invalida, intenta usar una contraseña "+
                                                "mayor a 4 caráteres.")
        return cd

    def clean(self):
        """
        Cleans the data and returns it.
        :return: the clean data.
        """
        cd = self.cleaned_data
        cd = self.clean_name(cd)
        cd = self.clean_password(cd)
        return cd


class LoginForm(AuthenticationForm):
    """
    The class for the form used for the login.
    Inherits form the AuthenticationForm.
    """
    def __init__(self, request,*args, **kwargs):
        super().__init__(request,*args,**kwargs)
        self.fields['username'].label = 'Escribe tu correo'
        self.fields['password'].label = 'Ingresa tu contraseña'

    class Meta(AuthenticationForm):
        """
        The meta class for the form.
        Uses the CustomUser model.
        """
        model = CustomUser
        fields=('username','password')

class CustomUserCreationForm(UserCreationForm):
    """
    Class for the form used to create a new user.
    Inherits from the UserCreationForm.
    """
    def __init__(self, *args, **kwargs):
        """Initiates the form and changes the label of the fields.
        """
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label  = 'Usuario'
#        self.fields['email'].label     = 'Correo Electrónico'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Confirma tu contraseña'

    class Meta(UserCreationForm):
        """
        The meta class for the user creation form.
        Uses the CustomUserthe model and specifies
        the fields to present in the form
        """
        model = CustomUser
        fields = ('username', 'email')
        widgets = {
          'username': forms.Textarea(attrs={'rows':1,
                                            'cols':60,
                                            'style':'resize:none;'}),
        }


class CustomUserChangeForm(UserChangeForm):
    """
    Class for the form used to make changes into a user.
    Inherits from the UserChangeForm.
    """
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
    """
    Class for the form used for the changes that the user may do
    to it's profile.
    """
    orcid = forms.CharField(label='ORCID')
    class Meta:
        """The Meta class for the form, it uses the Person model.
        """
        model=Person
        fields=('first_name','last_name','affiliation','state','degree','sni')
        labels = {
            'first_name' : _('Nombres'),
            'last_name'  : _('Apellidos'),
            'affiliation': _('Adscripción'),
            'state'      : _('Estado'),
            'degree'     : _('Título'),
            'sni'        : _('SNI')
        }

    def clean_name(self,cd):
        """
        Cleans the name and validates it.
        :return: the cleaned name after validating it.
        """
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
        """
        Initiates the form and changes the widget for some of the
        fields from the model to use a queryset.
        """
        super(ProfileForm, self).__init__(*args,**kwargs)
        self.fields['affiliation'].queryset = Affiliation.objects.all()
        self.fields['state'].queryset = State.objects.all()
        self.fields['degree'].queryset = Person.DEGREE_CHOICES
        self.fields['sni'].queryset = Person.SNI_CHOICES

class PublicationPetitionForm(forms.Form):
    """
    Class for the form to create a publication.
    """
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
    authors   = forms.MultipleChoiceField(label ='Autores')

    def __init__(self, *args, **kwargs):
        """
        Initiates the form and fills the journal and authors fields with information
        from the database.
        """
        super(PublicationPetitionForm, self).__init__(*args, **kwargs)
        J_CHOICES = ((journal.id, journal.__str__()) for journal in Journal.objects.all())
        self.fields['journal'].choices = J_CHOICES
        OPTIONS   = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['authors'].choices = OPTIONS

class TutorPetitionForm(forms.Form):
    tutors = forms.MultipleChoiceField(label ='Tutores')

    def __init__(self, *args, **kwargs):
        super(TutorPetitionForm, self).__init__(*args, **kwargs)
        OPTIONS   = ((tutor.id, tutor.person.__str__()) for tutor in Researcher.objects.all())
        self.fields['tutors'].choices = OPTIONS

class StudentPetitionForm(forms.Form):
    students = forms.MultipleChoiceField(label ='Estudiantes')

    def __init__(self, *args, **kwargs):
        super(StudentPetitionForm, self).__init__(*args, **kwargs)
        OPTIONS = ((student.id, student.person.__str__()) for student in Student.objects.all())
        self.fields['students'].choices = OPTIONS

class PublicationChangeForm(forms.ModelForm):
    """
    Class for the form used to make changes in a publication.
    """
    doi       = forms.CharField(label = 'DOI')
    title     = forms.CharField(label = 'Título', max_length = 200)
    authors   = forms.MultipleChoiceField(label= 'autores')

    class Meta:
        """
        The meta class of the form, it uses the Publication model.
        """
        model=Publication
        fields=('journal', 'volume','issue','date')
        labels = {
            'journal': _('Revista'),
            'volume' : _('Volumen'),
            'issue' : _('Número'),
            'date' : _('Fecha'),
        }
    def __init__(self,*args, **kwargs):
        """
        Initiates the form and fills the journal and authors fields
        with information from the database for the user to choose.
        """
        super(PublicationChangeForm, self).__init__(*args, **kwargs)
        self.fields['journal'].queryset = Journal.objects.all()
        OPTIONS   = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['authors'].choices = OPTIONS


class GroupPetitionForm(forms.Form):
    """
    Class for the form used to create a new Group or to change an existing one.
    """
    name = forms.CharField(label = 'Nombre', max_length = 200)
    members = forms.MultipleChoiceField(label= 'Miembros')

    def __init__(self, *args, **kwargs):
        """
        Initiates the class and fills the members field with choices from
        the database.
        """
        super(GroupPetitionForm, self).__init__(*args, **kwargs)
        OPTIONS = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['members'].choices = OPTIONS

class GrantPetitionForm(forms.Form):
    """
    Class for the form used to create a new Grant.
    """
    years = []
    for i in range (0, 20):
        years.append(2000+i)
    title        = forms.CharField(label = 'Título', max_length = 200)
    start_date   = forms.DateField(widget = forms.SelectDateWidget(years=years),
                                   label = 'Fecha Inicio')
    end_date     = forms.DateField(widget = forms.SelectDateWidget(years=years),
                                   label = 'Fecha Final', required = False)
    participants = forms.MultipleChoiceField(label= 'Miembros', required=False)

    def __init__(self, *args, **kwargs):
        """
        Initiates the form and fills the participants field with information
        from the database as choices.
        """
        super(GrantPetitionForm, self).__init__(*args, **kwargs)
        OPTIONS = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['participants'].choices = OPTIONS

class GrantChangeForm(forms.Form):
    """
    Class for the form used to make changes into a Grant.
    """
    years = []
    for i in range (0, 20):
        years.append(2000+i)
    start_date   = forms.DateField(widget = forms.SelectDateWidget(years=years),
                                   label = 'Fecha Inicio')
    end_date     = forms.DateField(widget = forms.SelectDateWidget(years=years),
                                   label = 'Fecha Final', required=False)
    participants = forms.MultipleChoiceField(label= 'Miembros', required=False)

    def __init__(self, *args, **kwargs):
        """
        Initiates the form and fills the participants fields with information
        from the database.
        """
        super(GrantChangeForm, self).__init__(*args, **kwargs)
        OPTIONS = ((person.id, person.__str__()) for person in Person.objects.all())
        self.fields['participants'].choices = OPTIONS

class AffiliationPetitionForm(forms.Form):
    """Class for the form used to create a new affiliation.
    """
    name        = forms.CharField(label = 'Nombre', max_length = 200)
    acronym     = forms.CharField(label = 'Acrónimo', max_length = 200, required = False)
    address     = forms.CharField(label = 'Dirección', max_length = 200)
    super_level = forms.ModelChoiceField(label = 'Nivel Superior', queryset = Affiliation.objects.all(), required = False)
