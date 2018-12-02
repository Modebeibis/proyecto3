from django.shortcuts import render,  redirect
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,  urlsafe_base64_decode
from django.template import RequestContext
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth import login
from django.template import RequestContext

from .forms import *
from .models import *

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
        user.person.save()
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
        individual = Person.objects.get(pk = group_member.person.id)
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
    print(member_of_groups)
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
        affiliations = Affiliation.objects.filter(name__icontains=q)
        publications = Publication.objects.filter(title__icontains=q)
        return render(request, 'core/search.html',
                      {'persons': persons,
                       'affiliations': affiliations,
                       'publications': publications,
                       'query': q})

    else:
        return HttpResponse('Please submit a search term.')


def profile_changes(request):
    print(request.method)
    person = Person.objects.get(user = request.user.id)
    if not request.user.is_authenticated:
        return render(request, 'core/profile.html')

    if request.method == 'POST':
        print('hola')
        form = ProfileForm(request.POST)
        if form.is_valid():
            print('hi')
            first_name   = form.cleaned_data.get('first_name')
            last_name    = form.cleaned_data.get('last_name')
            affiliations = Affiliation.objects.get(pk = form.cleaned_data.get('affiliations'))
            orcid        = form.cleaned_data.get('orcid')
            state        = State.objects.get(pk = form.cleaned_data.get('states'))
            degree       = form.cleaned_data.get('degree')
            sni          = form.cleaned_data.get('sni')

            person.first_name  = first_name
            person.last_name   = last_name
            person.affiliation = affiliation
            person.orcid       = orcid
            person.state       = state
            person.user        = request.user
            person.degree      = degree
            person.sni         = sni
            person.save()

            return redirect('core/profile/'+ str(profile.user.id))

    form = ProfileForm(initial={'first_name':  person.first_name,
                                'last_name':   person.last_name,
                                'affiliation': person.affiliation,
                                'orcid':       person.orcid,
                                'state':       person.state,
                                'degree':      person.degree,
                                'sni':         person.sni
                                })
    print('hello')
    return render(request, 'core/researcher.html', {'form':form}, RequestContext(request))

def get_publication_petition(request):
    if not request.user.is_authenticated:
        return render(request, 'core/home.html')

    if request.method == 'POST':
        petition_form = PublicationPetitionForm(request.POST)

        if petition_form.is_valid():
            title   = petition_form.cleaned_data.get('title')
            journal = Journal.objects.get(pk = petition_form.cleaned_data.get('journal'))
            volume  = petition_form.cleaned_data.get('volume')
            issue   = petition_form.cleaned_data.get('issue')
            date    = petition_form.cleaned_data.get('date')
            doi     = petition_form.cleaned_data.get('doi')
            authors_id = petition_form.cleaned_data.get('authors')

            if Publication.objects.filter(doi = doi).exists():
                publication = Publication.objects.get(doi = doi)
                return redirect('/publicacion/' + str(publication.id))

            petitioner = Person.objects.get(user = request.user.id)

            if petitioner.id not in authors_id:
                authors_id.append(petitioner.id)

            publication = Publication.objects.create(title   = title,
                                                     journal = journal,
                                                     volume  = volume,
                                                     issue   = issue,
                                                     date    = date,
                                                     doi     = doi)

            for author_id in authors_id:
                author = Person.objects.get(pk = author_id)
                AuthorOf.objects.create(publication = publication,
                                        person = author)

            return redirect('/publicacion/' + str(publication.id))

    petition_form = PublicationPetitionForm()
    return render(request, 'core/publication_petition.html',
                  {'form':petition_form}, RequestContext(request))

def publication_changes(request,publication_id):
    print('enter')
    if not request.user.is_authenticated:
        return render(request, 'core/home.html')

    if request.method == 'POST':
        print('POST')
        pub_instance=Publication.objects.get(pk = publication_id)
        form = PublicationChangeForm(request.POST, instance= pub_instance)

        if form.is_valid():
            print('valid')
            authors = form.cleaned_data.get('authors')
            title   = form.cleaned_data.get('title')
            doi     = form.cleaned_data.get('doi')
            publication = form.save(commit = False)
            publication.title = title
            publication.doi = doi
            publication.save()
            for author in authors:
                if AuthorOf.objects.filter(person = author,publication = publication).exists():
                    continue
                else:
                    AuthorOf.objects.create(publication = publication,
                                            person = author)
            return redirect('/publicacion/' + str(publication_id))
    print('get')
    publication = Publication.objects.get(pk= publication_id)
    form = PublicationChangeForm(initial={'title': publication.title,
                                         'journal': publication.journal,
                                         'volume': publication.volume,
                                         'issue': publication.issue,
                                         'date': publication.date,
                                         'doi': publication.doi})
    return render(request, 'core/publication_change.html',
                  {'form':form,
                  'publication': publication }, RequestContext(request))


def get_group_petition(request):
    if not request.user.is_authenticated:
        return render(request, 'core/home.html')

    if request.method == 'POST':
        petition_form = GroupPetitionForm(request.POST)

        if petition_form.is_valid():
            name = petition_form.cleaned_data.get('name')
            owner = Person.objects.get(user = request.user.id)
            members_id = petition_form.cleaned_data.get('members')

            group = Group.objects.create(name = name, owner = owner)

            for member_id in members_id:
                member = Person.objects.get(pk = member_id)
                GroupMember.objects.create(group = group,
                                           person = member)
            return redirect('/grupo/' + str(group.id))

    petition_form = GroupPetitionForm()
    return render(request, 'core/group_petition.html',
                  {'form':petition_form}, RequestContext(request))
