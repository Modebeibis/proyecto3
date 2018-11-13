from django.db import models

class Affiliation(models.Model):
    name        = models.TextField()
    super_level = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    address     = models.TextField()
    def __str__(self):
        if self.super_level is None:
            return self.name
        else:
            return '%s - %s' % (self.super_level.__str__(), self.name)

class Role(models.Model):
    description = models.TextField()
    def __str__(self):
        return self.description

class State(models.Model):
    name = models.TextField()
    def __str__(self):
        return self.name
    def relative_density(self):
        return Person.objects.filter(state=self).count()

class Person(models.Model):
    first_name  = models.TextField()
    last_name   = models.TextField()
    affiliation = models.ForeignKey(Affiliation, on_delete=models.PROTECT)
    email       = models.EmailField()
    orcid       = models.TextField(unique=True)
    role        = models.ForeignKey(Role, on_delete=models.PROTECT)
    state       = models.ForeignKey(State, on_delete=models.PROTECT)

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

    class Meta:
        unique_together = (('person'), ('role'),)

class Administrator(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    role   = models.ForeignKey(Role, on_delete=models.PROTECT)

# class AffiliationSublevel(models.Model):
#     sub = models.ForeignKey(
#         Affiliation,
#         related_name='sub',
#         on_delete=models.CASCADE
#     )
#     super = models.ForeignKey(
#         Affiliation,
#         related_name='super',
#         on_delete=models.CASCADE
#         )
#
#     class Meta:
#         unique_together = (('super', 'sub'),)

class Journal(models.Model):
    name = models.TextField(unique=True)
    issn = models.TextField(max_length=9, unique=True)
    def __str__(self):
        return self.name

class Publication(models.Model):
    title   = models.TextField()
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    volume  = models.IntegerField()
    issue   = models.IntegerField()
    date    = models.DateField()
    doi     = models.TextField(unique=True)
    def __str__(self):
        return self.title

class AuthorOf(models.Model):
    person      = models.ForeignKey(Person, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('person', 'publication'),)

class ExternalAuthor(models.Model):
    first_name = models.TextField()
    last_name  = models.TextField()
    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        unique_together = (('first_name', 'last_name'),)

class AuthorOfExternal(models.Model):
    author      = models.ForeignKey(ExternalAuthor, on_delete=models.PROTECT)
    publication = models.ForeignKey(Publication, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('author', 'publication'),)

class Researcher(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    role   = models.ForeignKey(Role, on_delete=models.PROTECT)

class Grant(models.Model):
    responsible = models.ForeignKey(Researcher, on_delete=models.CASCADE)
    title       = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField()
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
    role   = models.ForeignKey(Role, on_delete=models.PROTECT)

class Student(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    role   = models.ForeignKey(Role, on_delete=models.PROTECT)

class StudentOf(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    tutor   = models.ForeignKey(Researcher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'tutor'),)

class UserPetition(models.Model):
    name = models.TextField()
    first_surname = models.TextField()
    second_surname = models.TextField()
    email = models.TextField()

class AffiliationPetition(models.Model):
    name = models.TextField()
    email = models.TextField()
    address = models.TextField()
    id_super_level = models.ForeignKey(Affiliation, null = True, on_delete = models.SET_NULL)

class PublicationPetition(models.Model):
    id_researcher = models.ForeignKey(Researcher, on_delete = models.CASCADE)
    title   = models.TextField()
    journal = models.ForeignKey(Journal, on_delete=models.PROTECT)
    volume  = models.IntegerField()
    issue   = models.IntegerField()
    date    = models.DateField()
    doi     = models.TextField()

class JournalPetition(models.Model):
    id_researcher = models.ForeignKey(Researcher, on_delete = models.CASCADE)
    name = models.TextField()
    issn = models.TextField(max_length=9, unique=True)

class ExternalAuthorPetition(models.Model):
    first_name = models.TextField()
    last_name  = models.TextField()

class GroupPetition(models.Model):
    id_researcher = models.ForeignKey(Researcher, on_delete = models.CASCADE)
    name = models.TextField()

class GroupAddPetition(models.Model):
    id_researcher_owner = models.ForeignKey(Researcher, on_delete = models.CASCADE)
    id_person_to_add = models.ForeignKey(Person, on_delete = models.CASCADE)
    id_group = models.ForeignKey(Group, null = True, on_delete = models.SET_NULL)
    id_petition_group = models.ForeignKey(GroupPetition, null = True, on_delete = models.SET_NULL)

    def save(self, *args, **kwargs):
       """

       Checks that id_group and id_petition_group are not NULL at the same time.

       """
       if not id_group and not id_person_group:
           raise Exception("You can't have a group petition that points to no group.")
       super(self, GroupAddPetition).save(*args, **kwargs)
