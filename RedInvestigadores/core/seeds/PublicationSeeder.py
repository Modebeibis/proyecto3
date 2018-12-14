from faker import Faker
from core.models import Person, Journal, Publication, AuthorOf
from random import randint

class PublicationSeeder(object):

    def get_unique_doi(self):
        faker   = Faker()
        while True:
            doi = faker.isbn10()
            if not Publication.objects.filter(doi = doi).exists():
                return doi

    def seed(self):
        faker = Faker()

        for i in range(1000):
            title   = faker.sentence()
            journal = Journal.objects.get(pk = randint(1, 50))
            volume  = randint(1, 800)
            issue   = randint(1, 10)
            date    = faker.date()
            doi     = self.get_unique_doi()

            Publication.objects.get_or_create(title = title,
                                              journal = journal,
                                              volume = volume,
                                              issue = issue,
                                              date = date,
                                              doi = doi)
    def seed_authors(self):
        for i in range(1000):
            publication = Publication.objects.get(pk = i + 1)
            num_authors = randint(1, 8)
            for j in range(num_authors):
                while True:
                    person_id = randint(1, 500)
                    if not (AuthorOf.objects.filter(person = person_id,
                                                    publication = i + 1).exists()):
                        break

                person = Person.objects.get(pk = person_id)
                AuthorOf.objects.get_or_create(person = person,
                                               publication = publication)
