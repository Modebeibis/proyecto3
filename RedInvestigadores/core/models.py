from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator

class Affiliation(models.Model):
    """
    Affiliation class represents a model/relationship for the database.
    Each affiliation has a name, an acronym, an address and can have a superior level.
    When the superior level is deleted then the same happends for all dependent
    affiliations.
    If the affiliation has no superior level then the value NULL is assigned.
    """

    name        = models.TextField()
    acronym     = models.TextField(null=True, blank=True)
    super_level = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    address     = models.TextField()

    def __str__(self):
        """
        Returns a string representation of the affiliation.

        :return: a string representation of the affiliation.
        """

        if self.super_level is None:
            return self.name
        else:
            return '%s - %s' % (self.super_level.__str__(), self.name)

    def top_level(self):
        """
        Returns the superior level of an affiliation

        :return: the superior level of an affiliation
        """

        if self.super_level is None:
            return self
        else:
            return self.super_level.top_level()

    def pop_list_state(self, state):
        """
        Returns a list of inidivuals who belong to the affiliation and are
        located in the given state

        :param state: the given state
        :return: a list of individuals
        """

        population_list = []
        persons = Person.objects.all()
        for person in persons:
            if (person.affiliation.top_level() == self) and (person.state == state):
                population_list.append(person)
        return population_list

class Role(models.Model):
    """
    Role class represents a model/relationship for the database.
    Each role has a description.
    """

    description = models.TextField()

    def __str__(self):
        """
        Returns a string representation of the role.

        :return: a string representation of the role.
        """

        return self.description

class StateManager(models.Manager):
    """
    StateManager is a manage for the State model.
    """

    def max_population(self):
        """
        Calculates the maximum population of researchers/postdocs in the states.

        :return: the maximum population of researchers/postdocs in the states.
        """

        max = 0
        current = 0
        for state in State.objects.all():
            current = state.population()
            if current > max:
                max = state.population()
        return max

class State(models.Model):
    """
    State class represents a model/relationship for the database.
    Each state has a name and an StateManager object associated.
    """

    name = models.TextField()
    objects = StateManager()

    def __str__(self):
        """
        Returns a string representation of the state.

        :return: a string representation of the state.
        """

        return self.name

    def population(self):
        """
        Returns the number of persons in the state

        :return: the number of persons in the state
        """

        return Person.objects.filter(state=self).count()

    def relative_density(self):
        """
        Returns the relative density

        :return: the relative density
        """

        pop = self.population()
        if State.objects.max_population() == 0:
            return 0
        else:
            return pop / State.objects.max_population()

    def pop_list(self):
        """
        Returns a list of the individuals that are in the state

        :return: a list of the individuals that are in the state
        """

        user_persons = []
        every_person = Person.objects.filter(state=self)
        for person in every_person:
            if (not person.personrole_set.filter(role=4).exists()) or (not len(person.personrole_set.filter(role=4)) == 1):
                user_persons.append(person)
        return user_persons

    def affiliation_set(self):
        """
        Returns a set of the affiliations that are in the state

        :return: a set of the affiliations that are in the state
        """

        affiliations = set()
        for person in self.pop_list():
            affiliations.add(person.affiliation)
        return affiliations

    def affiliation_set_top(self):
        """
        Returns a set of the affiliations that are in the state and are top level

        :return: a set of the affiliations that are in the state and are top level
        """

        affiliations = set()
        for affiliation in self.affiliation_set():
            affiliations.add(affiliation.top_level())
        return affiliations

    def sub_affiliation_set(self, affiliation):
        """
        Returns a set of the affiliations that are in the state and are sub level

        :return: a set of the affiliations that are in the state and are sub level
        """

        affiliations = set()
        for person in self.pop_list():
            if person.affiliation.top_level() == affiliation:
                affiliations.add(person.affiliation)
        return affiliations


class CustomUser(AbstractUser):
    """
    CustomUser class represents a model/relationship for the database,
    in this case the user's relationship.
    Each user has an unique email, an unique username and a password.
    """

    email    = models.EmailField(_('email address'), unique=True)
    username = models.TextField(max_length=30, unique=True)
    password = models.TextField()

    def __str__(self):
        """
        Returns a string representation of the user.

        :return: a string representation of the user.
        """

        return self.email

class Person(models.Model):
    """
    Person class represents a model/relationship for the database.
    Each person has a first name, last name, an affiliation it belongs
    to, an unique orcid, a state where the person can be found,
    a degree, a SNI level and they must all confirm an email.
    If the user that is associated to is deleted then the same happends
    for the person.
    The state and affiliation must not be deleted.
    """

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
        """
        Returns a string representation of the person.

        :return: a string representation of the person.
        """

        return '%s %s' % (self.first_name, self.last_name)

class PersonRole(models.Model):
    """
    PersonRole class represents a model/relationship for the database.
    The class indicates what roles a person has, it is a many to many relationship
    that has been normalized using the 4NF.
    """

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        """
        Returns a string representation of the roles a person has.

        :return: a string representation of the roles a person has.
        """

        return ("(" + self.person.__str__()
                + "-" + self.person.user.__str__()
                + ", " + self.role.description + ")")

    class Meta:
        """
        Meta class for PersonRole
        """

        unique_together = (('person'), ('role'),)

class Administrator(models.Model):
    """
    Administrator class represents a model/relationship for the database.
    It contains all the persons who are administrators, it is a one to one
    relationship with the Person's relationship.
    """

    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the administrator.

        :return: a string representation of the administrator.
        """

        return "%s - %s" % (self.person.__str__(), self.person.user.__str__())

class Journal(models.Model):
    """
    Journal class represents a model/relationship for the database.
    Each journal has a name and an unique ISSN.
    """

    name = models.TextField(unique=True)
    issn = models.TextField(max_length=9, unique=True)

    def __str__(self):
        """
        Returns a string representation of the journal.

        :return: a string representation of the journal.
        """

        return self.name

class Publication(models.Model):
    """
    Publication class represents a model/relationship for the database.
    Each publication has a title, a journal it belongs to, a volume,
    an issue, a date and an unique DOI.
    The journal must not be deleted.
    """

    title   = models.TextField()
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    volume  = models.IntegerField(validators=[MinValueValidator(1)])
    issue   = models.IntegerField(validators=[MinValueValidator(0)])
    date    = models.DateField()
    doi     = models.TextField(unique=True)

    def __str__(self):
        """
        Returns a string representation of the publication.

        :return: a string representation of the publication.
        """

        return self.title

class AuthorOf(models.Model):
    """
    AuthorOf class represents a model/relationship for the database.
    The class indicates who are the author of a publication.
    It is a many to many relationship normalized with 4NF.
    """

    person      = models.ForeignKey(Person, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the author in a publication.

        :return: a string representation of the author in a publication.
        """

        return ("(" + self.person.__str__()
                + "-" + self.person.user.__str__()
                + ", " + self.publication.title + ")")

    class Meta:
        """
        Meta class for AuthorOf
        """

        unique_together = (('person', 'publication'),)

class Researcher(models.Model):
    """
    Researcher class represents a model/relationship for the database.
    It contains all the persons who are researchers, it is a one to one
    relationship with the Person's relationship.
    """

    person = models.OneToOneField(Person, on_delete=models.CASCADE)

    def __str__(self):
        """
        Returns a string representation of the researcher.

        :return: a string representation of the researcher.
        """

        return '%s - %s' % (person.__str__(), person.user.__str__())

class Grant(models.Model):
    """
    Grant class represents a model/relationship for the database.
    Each grant has a responsible, a title, and a start and end date.
    The end date can be nullable.
    In case the responsible is deleted then the same happends for the grant.
    """

    responsible = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    title       = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        Returns a string representation of the grant.

        :return: a string representation of the grant.
        """

        return self.title

    class Meta:
        """
        Meta class for Grant
        """

        unique_together = (('responsible', 'title'),)

class GrantParticipant(models.Model):
    """
    GrantParticipant class represents a model/relationship for the database.
    The class indicates who are the participants in a grant.
    It is a many to many relationship normalized with 4NF.
    """

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    grant  = models.ForeignKey(Grant, on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for GrantParticipant
        """
        unique_together = (('person', 'grant'),)

class Group(models.Model):
    """
    Group class represents a model/relationship for the database.
    Each group has a name and an owner.
    In case the owner is deleted, the group stays the same.
    """

    name  = models.TextField()
    owner = models.ForeignKey(Person, on_delete=models.DO_NOTHING)

    def __str__(self):
        """
        Returns a string representation of the group.

        :return: a string representation of the group.
        """

        return self.name

    class Meta:
        """
        Meta class for Group
        """

        unique_together = (('name', 'owner'),)

class GroupMember(models.Model):
    """
    GroupMember class represents a model/relationship for the database.
    The class indicates who are the members of a group.
    It is a many to many relationship normalized with 4NF.
    """

    group  = models.ForeignKey(Group, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for GroupMember
        """

        unique_together = (('group', 'person'),)

class Postdoc(models.Model):
    """
    Postdoc class represents a model/relationship for the database.
    It contains all the persons who are postdoc, it is a one to one
    relationship with the Person's relationship.
    """

    person = models.OneToOneField(Person, on_delete=models.CASCADE)

class Student(models.Model):
    """
    Student class represents a model/relationship for the database.
    It contains all the persons who are students, it is a one to one
    relationship with the Person's relationship.
    """

    person = models.OneToOneField(Person, on_delete=models.CASCADE)

class StudentOf(models.Model):
    """
    AuthorOf class represents a model/relationship for the database.
    The class indicates who is the student of a researcher.
    It is a many to many relationship normalized with 4NF.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor   = models.ForeignKey(Researcher, on_delete=models.CASCADE)

    class Meta:
        """
        Meta class for StudentOf
        """
        
        unique_together = (('student', 'tutor'),)

@receiver(post_save, sender = CustomUser)
def create_person_profile(sender, instance, created, **kwargs):
    """
    Trigger for when an user is created.
    It creates a person associated to the user
    and assigns it the researcher's role

    """
    if created:
        person  = Person.objects.create, and a start and end date.
                                _name,
                                In case the respoorcid      = str(instance),nsible is deleted then the same happends for the grant.
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
