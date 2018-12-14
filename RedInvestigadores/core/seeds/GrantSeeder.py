from faker import Faker
from core.models import Grant, GrantParticipant
from core.models import Person, Researcher
from random import randint

"""
Class to seed grants into the database.

"""

class GrantSeeder(object):
    """
    GrantSeeder is the one who has the capacity of creating N grants
    and inserting each one of them into the database, it also has the
    capacity to add random individuals to participate in this grants.

    """

    def seed(self):
        """
        Creates 100 different grants and inserts them into the database.
        Each of them follows the model a grant has:
        * responsible - Random researcher is selected
        * title       - Random sentence is given
        * start_date  - Random date_time is given
        * end_date    - Random date_time is given
        """

        faker = Faker()
        for i in range(100):
            responsible = Researcher.objects.get(pk = randint(1, 350))
            title = faker.sentence()
            start_date = faker.date_time()
            end_date = faker.date_time()

            Grant.objects.get_or_create(responsible = responsible,
                                        title = title,
                                        start_date = start_date,
                                        end_date = end_date)
    def seed_participants(self):
        """
        Creates 200 different participants and inserts them into the database.
        Each of them follows the model a grant participant has:
        * grant  - Random grant is selected
        * person - Random person is selected

        If the person is already participanting in the grant then another person
        and another grant is selected.
        """

        faker = Faker()
        for i in range(200):
            while True:
                person_id = randint(1, 500)
                grant_id = randint(1, 100)
                person = Person.objects.get(pk = person_id)
                grant = Grant.objects.get(pk = grant_id)
                if not (GrantParticipant.objects.filter(person = person,
                                                        grant = grant).exists()):
                    break

            GrantParticipant.objects.get_or_create(person = person,
                                                   grant = grant)
