from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse

from .forms import CustomUserCreationForm
from .models import Person, CustomUser, Affiliation, PersonRole, Role

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'login.html'

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
    persons = Person.objects.filter(affiliation = affiliation_id)
    register = []
    for person in persons:
        person_roles = PersonRole.objects.filter(person = person.id)
        roles = []
        for person_role in person_roles:
            roles.append(person_role.role)

        register.append(PersonInformation(person, roles))

    return render(request, 'core/sede.html',
                  {'affiliation': affiliation, 'register':register})

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
