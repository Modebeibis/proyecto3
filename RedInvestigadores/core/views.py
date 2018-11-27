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

from .forms import CustomLoginForm, CustomSignupForm, CustomUserCreationForm, ProfileForm
from .models import Person, CustomUser, Affiliation, PersonRole, Role, Publication, AuthorOf
from .models import Group, GroupMember, Grant, GrantParticipant, Researcher

from allauth.account.views import *
from allauth.account.forms import LoginForm, SignupForm

def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save(request)
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
        form = CustomSignupForm()
        lform = CustomLoginForm(request.POST)
    return render(request, 'login.html', {'form': form})

def account_activation_sent(request):
    return render(request, 'core/account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and not (user.is_active) and account_activation_token.check_token(user, token):
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

def get_grant(request, grant_id):
    grant = Grant.objects.get(pk = grant_id)
    responsible = Person.objects.get(pk = grant.responsible.person.id)
    grant_participants = GrantParticipant.objects.filter(grant = grant.id)
    participants = []
    for grant_participant in grant_participants:
        participant = Person.objects.get(pk = grant_participant.person.id)
        participants.append(participant)

    return render(request, 'core/grant.html',
                  {'grant': grant, 'responsible': responsible,
                   'participants':participants})

def get_group(request, group_id):
    group = Group.objects.get(pk = group_id)
    members = []
    members.append(Person.objects.get(pk = group.owner.id))
    group_members = GroupMember.objects.filter(group = group.id)
    for group_member in group_members:
        individual = Person.objects.get(pk = group_member.id)
        members.append(individual)

    return render(request, 'core/group.html',
                 {'group': group, 'members': members})

def get_publication(request, publication_id):
    publication = Publication.objects.get(pk = publication_id)
    authors_of = AuthorOf.objects.filter(publication = publication)
    authors = []
    for author_of in authors_of:
        author = Person.objects.get(pk = author_of.person.id)
        authors.append(author)

    return render(request, 'core/publication.html',
                  {'publication': publication, 'authors': authors})

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
    papers_author_of = AuthorOf.objects.filter(person = person)
    papers = []
    responsible_grants = []

    for paper_author in papers_author_of:
        paper = Publication.objects.get(pk = paper_author.publication.id)
        papers.append(paper)

    owner_of_groups = Group.objects.filter(owner = person.id)
    owner_groups = []
    for owner_of_group in owner_of_groups:
        owner_group = Group.objects.get(pk = owner_of_group.id)
        owner_groups.append(owner_group)

    member_of_groups = GroupMember.objects.filter(person = person.id)
    member_groups = []
    for member_of_group in member_of_groups:
        member_group = Group.objects.get(pk = member_of_group.group.id)
        member_groups.append(member_group)

    if (Researcher.objects.filter(person = person.id).exists()):
        researcher =  Researcher.objects.get(person = person.id)
        responsible_of_grants = Grant.objects.filter(responsible = researcher)
        responsible_grants = []
        for responsible_of_grant in responsible_of_grants:
            responsible_grant = Grant.objects.get(pk = responsible_of_grant.id)
            responsible_grants.append(responsible_grant)

    participant_of_grants = GrantParticipant.objects.filter(person = person)
    participant_grants = []
    for participant_of_grant in participant_of_grants:
        participant_grant = Grant.objects.get(pk = participant_of_grant.grant.id)
        participant_grants.append(participant_grant)

    return render(request, 'core/profile.html',
                  {'person': person,
                   'user': user,
                   'papers':papers,
                   'owner_groups':owner_groups,
                   'member_groups':member_groups,
                   'responsible_grants': responsible_grants,
                   'participant_grants': participant_grants})


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        persons = Person.objects.filter(first_name__icontains=q)
        return render(request, 'core/search.html',
                      {'persons': persons, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')

def profileChanges(request):
    if not request.user.is_authenticated:
        return render(request, 'core/home.html')
    if request.method == 'POST':
        form=ProfileForm(request.POST, instance=request.user.person)
        if form.is_valid():
            profile.save()
            return redirect('core/researcher/'+ str(profile.user.id))
    else:
        form = ProfileForm()
        return render(request, 'core/researcher.html')
