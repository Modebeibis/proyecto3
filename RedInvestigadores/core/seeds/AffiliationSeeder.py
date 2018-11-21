from faker import Faker
from core.models import Affiliation
from random import randint

class AffiliationSeeder(object):

    def seed(self):
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
