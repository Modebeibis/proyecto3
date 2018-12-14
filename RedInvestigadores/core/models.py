from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator

class Affiliation(models.Model):
    name        = models.TextField()
    acronym     = models.TextField(null=True, blank=True)
    super_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    address     = models.TextField()

    def __str__(self):
        if self.super_level is None:
            return self.name
        else:
            return '%s - %s' % (self.super_level.__str__(), self.name)

    def top_level(self):
        if self.super_level is None:
            return self
        else:
            return self.super_level.top_level()

    def pop_list_state(self, state):
        population_list = []
        persons = Person.objects.all()
        for person in persons:
            if (person.affiliation.top_level() == self) and (person.state == state):
                population_list.append(person)
        return population_list

class Role(models.Model):
    description = models.TextField()
    def __str__(self):
        return self.description

class StateManager(models.Manager):
    def max_population(self):
        '''

        Calculates the maximum population of researchers/postdocs in the states.

        '''
        max = 0
        current = 0
        for state in State.objects.all():
            current = state.population()
            if current > max:
                max = state.population()
        return max

class State(models.Model):
    name = models.TextField()
    objects = StateManager()

    def __str__(self):
        return self.name

    def population(self):
        return Person.objects.filter(state=self).count()

    def relative_density(self):
        pop = self.population()
        if State.objects.max_population() == 0:
            return 0
        else:
            return pop / State.objects.max_population()

    def pop_list(self):
        user_persons = []
        every_person = Person.objects.filter(state=self)
        for person in every_person:
            if (not person.personrole_set.filter(role=4).exists()) or (not len(person.personrole_set.filter(role=4)) == 1):
                user_persons.append(person)
        return user_persons

    def affiliation_set(self):
        affiliations = set()
        for person in self.pop_list():
            affiliations.add(person.affiliation)
        return affiliations

    def affiliation_set_top(self):
        affiliations = set()
        for affiliation in self.affiliation_set():
            affiliations.add(affiliation.top_level())
        return affiliations

    def sub_affiliation_set(self, affiliation):
        affiliations = set()
        for person in self.pop_list():
            if person.affiliation.top_level() == affiliation:
                affiliations.add(person.affiliation)
        return affiliations


class CustomUser(AbstractUser):
    email    = models.EmailField(_('email address'), unique=True)
    username = models.TextField(max_length=30, unique=True)
    password = models.TextField()

    def __str__(self):
        return self.email

class Person(models.Model):
    first_name      = models.CharField(max_length=200)
    last_name       = models.CharField(max_length=200)
    affiliation     = models.ForeignKey(Affiliation, default=1, on_delete=models.PROTECT)
    orcid           = models.TextField(unique=True)
    state           = models.ForeignKey(State, default=1, on_delete=models.PROTECT)
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    BACHELOR = 'BSC'
    MASTERS  = 'MSC'
    DOCTORAL = 'PHD'
    DEGREE_CHOICES = (
        (BACHELOR, 'Licenciatura'),
        (MASTERS,  'Maestría'),
        (DOCTORAL, 'Doctorado'),
    )
    degree = models.CharField(
        max_length=3,
        choices=DEGREE_CHOICES,
        default=BACHELOR
    )

    NOT_A_MEMBER = 'N'
    CANDIDATE    = 'C'
    LEVEL_I      = '1'
    LEVEL_II     = '2'
    LEVEL_III    = '3'
    EMERITUS     = 'E'
    SNI_CHOICES = (
        (NOT_A_MEMBER, 'No pertenece'),
        (CANDIDATE,    'Candidato'),
        (LEVEL_I,      'Nivel I'),
        (LEVEL_II,     'Nivel II'),
        (LEVEL_III,    'Nivel III'),
        (EMERITUS,     'Emérito'),
    )
    sni = models.CharField(
        max_length=1,
        choices=SNI_CHOICES,
        default=NOT_A_MEMBER
    )

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class PersonRole(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    def __str__(self):
        return ("(" + self.person.__str__()
                + "-" + self.person.user.__str__()
                + ", " + self.role.description + ")")

    class Meta:
        unique_together = (('person'), ('role'),)

class Administrator(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    def __str__(self):
        return "%s - %s" % (self.person.__str__(), self.person.user.__str__())

class Journal(models.Model):
    name = models.TextField(unique=True)
    issn = models.TextField(max_length=9, unique=True)
    def __str__(self):
        return self.name

class Publication(models.Model):
    title   = models.TextField()
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    volume  = models.IntegerField(validators=[MinValueValidator(1)])
    issue   = models.IntegerField(validators=[MinValueValidator(0)])
    date    = models.DateField()
    doi     = models.TextField(unique=True)
    def __str__(self):
        return self.title

class AuthorOf(models.Model):
    person      = models.ForeignKey(Person, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        return ("(" + self.person.__str__()
                + "-" + self.person.user.__str__()
                + ", " + self.publication.title + ")")

    class Meta:
        unique_together = (('person', 'publication'),)

class Researcher(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    def __str__(self):
        return '%s - %s' % (self.person.__str__(), self.person.user.__str__())

class Grant(models.Model):
    responsible = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    title       = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True)
    def __str__(self):
        return self.title

    class Meta:
        unique_together = (('responsible', 'title'),)

class GrantParticipant(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    grant  = models.ForeignKey(Grant, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('person', 'grant'),)

class Group(models.Model):
    name  = models.TextField()
    owner = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name', 'owner'),)

class GroupMember(models.Model):
    group  = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('group', 'person'),)

class Postdoc(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)

class Student(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    def __str__(self):
        return self.person.__str__()

class StudentOf(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor   = models.ForeignKey(Researcher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'tutor'),)

@receiver(post_save, sender = CustomUser)
def create_person_profile(sender, instance, created, **kwargs):
    """
    Trigger for when an user is created.
    It creates a person associated to the user
    and assigns it the researcher's role

    """
    if created:
        person  = Person.objects.create(first_name = instance.first_name,
                                        last_name  = instance.last_name,
                                        orcid      = str(instance),
                                        user       = instance)
        role = Role.objects.get(pk = 3)
        PersonRole.objects.create(person = person, role = role)
        Researcher.objects.create(person = person)

@receiver(post_save, sender = Administrator)
def setup_credentials_and_role(sender, instance, created, **kwargs):
    """
    Trigger for adding the Administrator role, and
    assigning the corresponding credentials to a newly
    created Administrator
    """
    if created:
        instance.person.user.is_staff     = True
        instance.person.user.is_superuser = True
        instance.person.user.save(update_fields=['is_staff', 'is_superuser'])
        role = Role.objects.get(pk = 4)
        PersonRole.objects.get_or_create(person = instance.person,
                                         role   = role)

@receiver(post_delete, sender = Administrator)
def delete_credentials_and_role(sender, instance, **kwargs):
    """
    Trigger for adding the Administrator role, and
    assigning the corresponding credentials to a newly
    created Administrator
    """
    instance.person.user.is_staff     = False
    instance.person.user.is_superuser = False
    instance.person.user.save(update_fields=['is_staff', 'is_superuser'])
    role = Role.objects.get(pk = 4)
    relation = PersonRole.objects.get(person = instance.person,
                                      role   = role)
    relation.delete()
