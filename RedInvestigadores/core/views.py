from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login
from .forms import CustomLoginForm, CustomUserCreationForm
from .models import Person, CustomUser, Affiliation, PersonRole, Role

from allauth.account.views import *
from allauth.account.forms import LoginForm, SignupForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('core/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('core/account_activation_sent')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'core/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.person.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'core/account_activation_invalid.html')

class PersonInformation(object):
    def __init__(self, person, roles):
        self.person = person
        self.roles = roles

def home(request):
    return render(request, 'core/home.html')

def research(request):
    return render(request, 'core/researcher.html')

def about_of(request):
    return render(request, 'core/about_of.html')

def search_view(request):
    return render(request, 'core/search_view.html')

def list_profiles(request):
    return render(request, 'core/list_profiles.html')

def get_affiliations(request):
    affiliations = Affiliation.objects.all()
    return render(request, 'core/sedes.html', {'affiliations':affiliations})

def get_affiliation(request, affiliation_id):
    affiliation = Affiliation.objects.get(pk = affiliation_id)
    sub_levels = Affiliation.objects.filter(super_level = affiliation)
    persons = Person.objects.filter(affiliation = affiliation_id)
    register = []
    for person in persons:
        person_roles = PersonRole.objects.filter(person = person.id)
        roles = []
        for person_role in person_roles:
            roles.append(person_role.role)

        register.append(PersonInformation(person, roles))

    return render(request, 'core/sede.html',
                  {'affiliation': affiliation, 'sub_levels':sub_levels, 'register':register})

def get_user_profile(request, user_id):
    user = CustomUser.objects.get(pk = user_id)
    person = Person.objects.get(user = user_id)
    return render(request, 'core/profile.html',
                  {'person': person, 'user': user})


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        persons = Person.objects.filter(first_name__icontains=q)
        return render(request, 'core/search.html',
                      {'persons': persons, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
