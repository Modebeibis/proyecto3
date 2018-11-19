from faker import Faker
from core.models import Journal
from random import randint

class JournalSeeder(object):
    def seed(self):
        faker = Faker()

        for i in range(50):
            name = faker.company(),
            issn = faker.isbn10()

            Journal.objects.get_or_create(name = name,
                                          issn = issn)
