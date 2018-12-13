from faker import Faker
from core.models import Journal
from random import randint

class JournalSeeder(object):
    def get_unique_name(self):
        faker   = Faker()
        while True:
            name = faker.company()
            if not CustomUser.objects.filter(name = name).exists():
                return name

    def get_unique_issn(self):
        faker   = Faker()
        while True:
            issn = faker.isbn10()
            if not Person.objects.filter(issn = issn).exists():
                return issn

    def seed(self):
        for i in range(50):
            name = self.get_unique_name()
            issn = self.get_unique_issn()

            Journal.objects.get_or_create(name = name,
                                          issn = issn)
