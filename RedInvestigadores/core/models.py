from django.db import models

class Affiliation(models.Model):
    name        = models.TextField()
    super_level = models.ForeignKey('self', on_delete=models.CASCADE)
    address     = models.TextField()
    def __str__(self):
        if self.id < 3:
            return self.name
        else:
            return '%s - %s' % (self.super_level.__str__(), self.name)

class Role(models.Model):
    description = models.TextField()
    def __str__(self):
        return self.description

class Person(models.Model):
    first_name  = models.TextField()
    last_name   = models.TextField()
    affiliation = models.ForeignKey(Affiliation, on_delete=models.PROTECT)
    email       = models.EmailField()
    orcid       = models.TextField(unique=True)
    role        = models.ForeignKey(Role, on_delete=models.PROTECT)

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

    AGUASCALIENTES      = 'AGS'
    BAJA_CALIFORNIA     = 'BC'
    BAJA_CALIFORNIA_SUR = 'BCS'
    CAMPECHE            = 'CAMP'
    CHIAPAS             = 'CHIS'
    CHIHUAHUA           = 'CHIH'
    CIUDAD_DE_MEXICO    = 'CDMX'
    COAHUILA            = 'COAH'
    COLIMA              = 'COL'
    DURANGO             = 'DGO'
    GUANAJUATO          = 'GTO'
    GUERRERO            = 'GRO'
    HIDALGO             = 'HGO'
    JALISGO             = 'JAL'
    MEXICO              = 'MEX'
    MICHOACAN           = 'MICH'
    MORELOS             = 'MOR'
    NAYARIT             = 'NAY'
    NUEVO_LEON          = 'NL'
    OAXACA              = 'OAX'
    PUEBLA              = 'PUE'
    QUERETARO           = 'QRO'
    QUINTANA_ROO        = 'QR'
    SAN_LUIS_POTOSI     = 'SLP'
    SINALOA             = 'SIN'
    SONORA              = 'SON'
    TABASCO             = 'TAB'
    TAMAULIPAS          = 'TAMPS'
    TLAXCALA            = 'TLAX'
    VERACRUZ            = 'VER'
    YUCATAN             = 'YUC'
    ZACATECAS           = 'ZAC'
    STATE_CHOICES = (
        (AGUASCALIENTES,      'Aguascalientes'),
        (BAJA_CALIFORNIA,     'Baja California'),
        (BAJA_CALIFORNIA_SUR, 'Baja California Sur'),
        (CAMPECHE,            'Campeche'),
        (CHIAPAS,             'Chiapas'),
        (CHIHUAHUA,           'Chihuahua'),
        (CIUDAD_DE_MEXICO,    'Ciudad de México'),
        (COAHUILA,            'Coahuila'),
        (COLIMA,              'Colima'),
        (DURANGO,             'Durango'),
        (GUANAJUATO,          'Guanajuato'),
        (GUERRERO,            'Guerrero'),
        (HIDALGO,             'Hidalgo'),
        (JALISGO,             'Jalisco'),
        (MEXICO,              'Estado de México'),
        (MICHOACAN,           'Michoacán'),
        (MORELOS,             'Morelos'),
        (NAYARIT,             'Nayarit'),
        (NUEVO_LEON,          'Nuevo León'),
        (OAXACA,              'Oaxaca'),
        (PUEBLA,              'Puebla'),
        (QUERETARO,           'Querétaro'),
        (QUINTANA_ROO,        'Quintana Roo'),
        (SAN_LUIS_POTOSI,     'San Luis Potosí'),
        (SINALOA,             'Sinaloa'),
        (SONORA,              'Sonora'),
        (TABASCO,             'Tabasco'),
        (TAMAULIPAS,          'Tamaulipas'),
        (TLAXCALA,            'Tlaxcala'),
        (VERACRUZ,            'Veracruz'),
        (YUCATAN,             'Yucatán'),
        (ZACATECAS,           'Zacatecas'),
    )
    state = models.CharField(
        max_length=4,
        choices=STATE_CHOICES,
        default=CIUDAD_DE_MEXICO
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
