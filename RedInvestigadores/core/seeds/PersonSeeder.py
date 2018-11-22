from faker import Faker
from core.models import Affiliation, Role, State
from core.models import CustomUser, Person, PersonRole, Administrator, Postdoc, Student, StudentOf, Researcher
from django.contrib.auth.hashers import make_password
from random import randint

class PersonSeeder(object):

    def seed(self):
        faker = Faker()

        for i in range(500):
            first_name  = faker.first_name()
            last_name   = faker.last_name()
            affiliation = Affiliation.objects.get(pk = randint(1, 70))
            email       = faker.email()
            orcid       = faker.isbn10()
            role        = Role.objects.get(pk = randint(1, 4))
            state       = State.objects.get(pk = randint(1, 29))

            username = "user%d" % (i+1)
            user     = CustomUser.objects.get_or_create(username = username,
                                                        password = make_password("pw%d" % (i+1)),
                                                        email    = email)

            Person.objects.get_or_create(first_name = first_name,
                                 last_name   = last_name,
                                 affiliation = affiliation,
                                 orcid       = orcid,
                                 role        = role,
                                 state       = state,
                                 user        = CustomUser.objects.get(username=username))

    def seed_admins(self):
        faker = Faker()
        role = Role.objects.get(pk = 4)

        for i in range(25):
            while True:
                person_id = randint(1, 50)
                if not Administrator.objects.filter(pk = person_id).exists():
                    break

            person = Person.objects.get(pk = person_id)
            user = CustomUser.objects.get(pk = person.user_id)

            user.is_staff = user.is_superuser = True
            user.save()

            PersonRole.objects.get_or_create(person = person,
                                             role   = role)

            Administrator.objects.get_or_create(person = person)

    def seed_researchers(self):
        faker = Faker()
        role = Role.objects.get(pk = 3)

        for i in range(25, 375):
            person = Person.objects.get(pk = (i+1))

            PersonRole.objects.get_or_create(person = person,
                                             role   = role)

            Researcher.objects.get_or_create(person = person)

    def seed_postdocs(self):
        faker = Faker()
        role = Role.objects.get(pk = 2)

        for i in range(150):
            while True:
                person_id = randint(25, 400)
                if not Postdoc.objects.filter(pk = person_id).exists():
                    break

            person = Person.objects.get(pk = person_id)

            PersonRole.objects.get_or_create(person = person,
                                             role   = role)

            Postdoc.objects.get_or_create(person = person)

    def seed_students(self):
        faker = Faker()
        role = Role.objects.get(pk = 1)

        for i in range(400, 500):
            person = Person.objects.get(pk = (i+1))

            PersonRole.objects.get_or_create(person = person,
                                             role   = role)

            Student.objects.get_or_create(person = person)

    def seed_student_of_relationships(self):
        faker = Faker()

        for i in range(100):
            student = Student.objects.get(pk = (i+1))

            while True:
                researcher_id = randint(1, 350)
                researcher = Researcher.objects.get(pk   = researcher_id)
                if not (StudentOf.objects.filter(student = student,
                                                 tutor   = researcher).exists()):
                    break

            StudentOf.objects.get_or_create(student = student,
                                            tutor   = researcher)

    def fill_person_and_roles(self):
        for i in range(500):
            if not PersonRole.objects.filter(person = (i+1)).exists():
                random_role = randint(1, 4)
                role = Role.objects.get(pk = random_role)
                person = Person.objects.get(pk = (i+1))

                PersonRole.objects.get_or_create(person = person,
                                                 role   = role)

                if (random_role == 1):
                    Student.objects.get_or_create(person = person)
                elif (random_role == 2):
                    Postdoc.objects.get_or_create(person = person)
                elif (random_role == 3):
                    Researcher.objects.get_or_create(person = person)
                else:
                    user = CustomUser.objects.get(pk = person.user_id)

                    user.is_staff = user.is_superuser = True
                    user.save()
                    Administrator.objects.get_or_create(person = person)
