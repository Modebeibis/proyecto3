from faker import Faker
from core.models import Journal
from random import randint

"""
Class to seed journals into the database.

"""

class JournalSeeder(object):
    """
    JournalSeeder is the one who has the capacity of creating
    N different journals and inserting each one of them into
    the database.

    """

    def get_unique_name(self):
        """
        Returns a journal's name that hasn't already been used in the database.

        :return: An unique name for the journal
        """

        faker   = Faker()
        while True:
            name = faker.company()
            if not Journal.objects.filter(name = name).exists():
                return name

    def get_unique_issn(self):
        """
        Returns a journal's issn that hasn't already been used in the database.

        :return: An unique issn for the journal
        """

        faker   = Faker()
        while True:
            issn = faker.isbn10()
            if not Journal.objects.filter(issn = issn).exists():
                return issn

    def seed(self):
        """
        Creates 50 different journals and inserts them into the database.
        Each of them follows the model a journal has:
        * name - An unique and random company name is given
        * issn - An unique and random isbn10 code is given
        """

        for i in range(50):
            name = self.get_unique_name()
            issn = self.get_unique_issn()

            Journal.objects.get_or_create(name = name,
                                          issn = issn)
