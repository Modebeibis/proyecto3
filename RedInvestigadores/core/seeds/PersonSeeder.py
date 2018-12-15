from faker import Faker
from core.models import Affiliation, Role, State
from core.models import CustomUser, Person, PersonRole, Administrator, Postdoc, Student, StudentOf, Researcher
from django.contrib.auth.hashers import make_password
from random import randint

"""
Class to seed persons into the database.

"""

class PersonSeeder(object):
    """
    PersonSeeder is the one who has the capacity of creating
    N persons and inserting each one of them into the database.

    """

    def get_unique_email(self):
        """
        Returns an user's email that hasn't already been used in the database.

        :return: An unique email for the person.
        """

        faker   = Faker()
        while True:
            email = faker.email()
            if not CustomUser.objects.filter(email = email).exists():
                return email

    def get_unique_orcid(self):
        """
        Returns an user's orcid that hasn't already been used in the database.

        :return: An unique orcid for the person.
        """

        faker   = Faker()
        while True:
            orcid = faker.isbn10()
            if not Person.objects.filter(orcid = orcid).exists():
                return orcid

    def seed(self):
        """
        Creates 500 persons, each with an unique email,
        and inserts them into the database.
        First the user is created, the trigger activates creating a person,
        the person is selected and it is filled with the given information.

        Each user follows the model a custom user has:
        * username - The password always follows the following: "userX"
                     Where X is the user's id
        * password - The password always follows the following: "pwX"
                     Where X is the user's id
        * email    - A random and unique email is given

        Each persons follows the model a person has:
        * first_name      - Random first name is given
        * last_name       - Random last name is given
        * affiliation     - Random affiliation is selected
        * degree          - Random degree is selected
        * orcid           - A random and unique orcid is given
        * sni             - A random SNI level is selected
        * state           - A random state is selected
        * user            - User is selected
        * email_confirmed - It is supposed that the email was already confirmed

        """

        faker   = Faker()
        degrees = ["BSC", "MSC", "PHD"]
        sni     = ["N", "C", "1", "2", "3", "E"]

        for i in range(500):
            first_name  = faker.first_name()
            last_name   = faker.last_name()
            affiliation = Affiliation.objects.get(pk = randint(1, 70))
            email       = self.get_unique_email()
            orcid       = self.get_unique_orcid()
            state       = State.objects.get(pk = randint(1, 32))

            username = "user%d" % (i+1)
            user     = CustomUser.objects.get_or_create(username = username,
                                                        password = make_password("pw%d" % (i+1)),
                                                        email    = email)

            person = Person.objects.get(pk=(i+1))
            person.first_name      = first_name
            person.last_name       = last_name
            person.affiliation     = affiliation
            person.degree          = degrees[randint(0,2)]
            person.orcid           = orcid
            person.sni             = sni[randint(0, 5)]
            person.state           = state
            person.user            = CustomUser.objects.get(username=username)
            person.email_confirmed = True
            person.save()

    def seed_admins(self):
        """
        Creates 25 administrators and inserts them into the database.
        Each administrator follows the model an administrator has:
        * person - Random person is selected

        If the person is already an administrator then another one is selected.
        """

        faker = Faker()
        role = Role.objects.get(pk = 4)

        for i in range(25):
            while True:
                person_id = randint(1, 50)
                if not Administrator.objects.filter(pk = person_id).exists():
                    break

            person = Person.objects.get(pk = person_id)
            user = CustomUser.objects.get(pk = person.user_id)

            user.save()

            Administrator.objects.get_or_create(person = person)

    def seed_researchers(self):
        """
        Creates 350 researchers and inserts them into the database.
        Each researcher follows the model a researcher has:
        * person - Random person is selected

        It also creates a PersonRole object to indicate that person is indeed
        a researcher.
        """

        faker = Faker()
        role = Role.objects.get(pk = 3)

        for i in range(25, 375):
            person = Person.objects.get(pk = (i+1))

            PersonRole.objects.get_or_create(person = person,
                                             role   = role)

            Researcher.objects.get_or_create(person = person)

    def seed_postdocs(self):
        """
        Creates 150 postdocs and inserts them into the database.
        Each postdoc follows the model a postdoc has:
        * person - Random person is selected

        If the person is already a postdoc then another one is selected.
        It also creates a PersonRole object to indicate that person is indeed
        a postdoc.
        """

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
        """
        Creates 100 students and inserts them into the database.
        Each student follows the model a student has:
        * person - Random person is selected

        If the person is already a student then another one is selected.
        It also creates a PersonRole object to indicate that person is indeed
        a student.
        """

        faker = Faker()
        role = Role.objects.get(pk = 1)

        for i in range(400, 500):
            person = Person.objects.get(pk = (i+1))

            PersonRole.objects.get_or_create(person = person,
                                             role   = role)

            Student.objects.get_or_create(person = person)

    def seed_student_of_relationships(self):
        """
        Creates 100 relationships between researchers and students.
        If a researcher is already in charge of a student, then another one is selected.
        """

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
        """
        Checks that each person in the database has at least one role.
        If it doesn't then it creates one. 
        """

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
