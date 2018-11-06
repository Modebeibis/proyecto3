from django.db import models

class Affiliations(models.Model):
    name    = models.TextField()
    address = models.TextField()

class Degrees(models.Model):
    degree = models.TextField()

class Roles(models.Model):
    description = models.TextField()

class SNI(models.Model):
    level = models.TextField()

class States(models.Model):
    name = models.TextField()

class Persons(models.Model):
    name        = models.TextField()
    last_name   = models.TextField()
    orcid       = models.TextField()
    email       = models.EmailField()
    affiliation = models.ForeignKey(Affiliations, on_delete=models.DO_NOTHING)
    degree      = models.ForeignKey(Degrees, on_delete=models.PROTECT)
    role        = models.ForeignKey(Roles, on_delete=models.PROTECT)
    state       = models.ForeignKey(States, on_delete=models.PROTECT)
    sni         = models.ForeignKey(SNI, on_delete=models.PROTECT)

class Administrators(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE)
    role   = models.ForeignKey(Roles, on_delete=models.PROTECT)

class Affiliation_sublevel(models.Model):
    sub   = models.ForeignKey(
        Affiliations,
        related_name='sub',
        on_delete=models.CASCADE
    )
    super = models.ForeignKey(
        Affiliations,
        related_name='super',
        on_delete=models.CASCADE
        )

    class Meta:
        unique_together = (('super', 'sub'),)

class Journals(models.Model):
    name = models.TextField()
    issn = models.TextField()

class Publications(models.Model):
    title   = models.TextField()
    journal = models.ForeignKey(Journals, on_delete=models.PROTECT)
    volume  = models.IntegerField()
    issue   = models.IntegerField()
    date    = models.DateField()
    doi     = models.TextField()

class Author_of(models.Model):
    person      = models.ForeignKey(Persons, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publications, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('person', 'publication'),)

class External_authors(models.Model):
    name      = models.TextField()
    last_name = models.TextField()

class Author_of_external(models.Model):
    author      = models.ForeignKey(External_authors, on_delete=models.PROTECT)
    publication = models.ForeignKey(Publications, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('author', 'publication'),)

class External_publications(models.Model):
    doi = models.TextField()

class External_citation(models.Model):
    cited  = models.ForeignKey(Publications, on_delete=models.CASCADE)
    citing = models.ForeignKey(External_publications, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('cited', 'citing'),)

class Researchers(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE)
    role   = models.ForeignKey(Roles, on_delete=models.PROTECT)

class Grants(models.Model):
    responsible = models.ForeignKey(Researchers, on_delete=models.CASCADE)
    title       = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField()

class Grant_participant(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE)
    grant  = models.ForeignKey(Grants, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('person', 'grant'),)

class Groups(models.Model):
    name  = models.TextField()
    owner = models.ForeignKey(Persons, on_delete=models.DO_NOTHING)

class Group_member(models.Model):
    group  = models.ForeignKey(Groups, on_delete=models.CASCADE)
    person = models.ForeignKey(Persons, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('group', 'person'),)

class Internal_citation(models.Model):
    cited  = models.ForeignKey(
        Publications,
        related_name='cited',
        on_delete=models.CASCADE
    )
    citing = models.ForeignKey(
        Publications,
        related_name='citing',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('cited', 'citing'),)

class PNPC(models.Model):
    level = models.TextField()

class Programs(models.Model):
    name        = models.TextField()
    affiliation = models.ForeignKey(Affiliations, on_delete=models.CASCADE)
    degree      = models.ForeignKey(Degrees, on_delete=models.PROTECT)
    pnpc        = models.ForeignKey(PNPC, on_delete=models.PROTECT)

class Program_tutor(models.Model):
    person  = models.ForeignKey(Persons, on_delete=models.CASCADE)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('person', 'program'),)

class Postdocs(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE)
    role   = models.ForeignKey(Roles, on_delete=models.PROTECT)

class Subjects(models.Model):
    classification = models.TextField()

class Publication_subject(models.Model):
    publication = models.ForeignKey(Publications, on_delete=models.CASCADE)
    subject     = models.ForeignKey(Subjects, on_delete=models.PROTECT)

    class Meta:
        unique_together = (('publication', 'subject'),)

class Students(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE)
    role   = models.ForeignKey(Roles, on_delete=models.PROTECT)

class Student_in(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'program'),)

class Student_of(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    tutor   = models.ForeignKey(Researchers, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'tutor'),)
