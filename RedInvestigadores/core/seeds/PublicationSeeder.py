from faker import Faker
from core.models import Person, Journal, Publication, AuthorOf
from random import randint

"""
Class to seed publications into the database.

"""

class PublicationSeeder(object):
    """
    PersonSeeder is the one who has the capacity of creating
    N different publications and inserting each one of them into the database.

    """

    def get_unique_doi(self):
        """
        Returns a publication's DOI that hasn't already been used in the database.

        :return: An unique DOI for the publication.
        """

        faker   = Faker()
        while True:
            doi = faker.isbn10()
            if not Publication.objects.filter(doi = doi).exists():
                return doi

    def seed(self):
        """
        Creates 1000 different publications and inserts them into the database.
        Each of them follows the model a publication has:
        * title   - Random sentence is given
        * journal - Random journal is selected
        * volume  - Random integer between 1 and 800 is selected
        * issue   - Random integer between 1 and 10 is selected
        * date    - Random Date is given
        * doi     - An unique and random isbn10 is given
        """

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
        """
        For each publication a number of authors is randomly chosen.
        Each of them follows the model an author has:
        * publication - Publication selected
        * person      - Random person is selected
        """

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
