from faker import Faker
from core.models import Affiliation
from random import randint

"""
Class to seed affiliations into the database.

"""

class AffiliationSeeder(object):
    """
    AffiliationSeeder is the one who has the capacity of creating N affiliations
    and inserting each one of them into the database.

    """

    def seed(self):
        """
        Creates 70 different affiliations and inserts them into the database.
        Each of them follows the model an affiliation has:
        * name        - Random company name is given
        * address     - Random address is given
        * super_level - The first 10 affiliations have no super level affiliation,
                        however the next 25 of them are have as a superior level one of
                        the previous ones that were created. And the same is applied for
                        the affiliations left.
        """

        faker = Faker()

        for i in range(70):
            name = faker.company()
            if (i <= 10):
                super_level = None
            elif (10 < i <= 35):
                super_level = Affiliation.objects.get(pk = randint(1, 10))
            else:
                super_level = Affiliation.objects.get(pk = randint(11, 35))

            address = faker.address()

            Affiliation.objects.get_or_create(name = name,
                                              super_level = super_level,
                                              address = address)
