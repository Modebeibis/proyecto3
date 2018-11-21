from faker import Faker
from core.models import Grant, GrantParticipant
from core.models import Person, Researcher
from random import randint

class GrantSeeder(object):

    def seed(self):
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
