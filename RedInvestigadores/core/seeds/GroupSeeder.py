from faker import Faker
from core.models import Group, GroupMember, Person
from random import randint

class GroupSeeder(object):
    def seed(self):
        faker = Faker()
        for i in range(200):
            name = faker.company()
            owner = Person.objects.get(pk = randint(1, 350))

            Group.objects.get_or_create(name = name,
                                        owner = owner)

    def seed_members(self):
        for i in range(200):
            group = Group.objects.get(pk = i + 1)
            num_members = randint(1, 10)
            for j in range(num_members):
                while True:
                    person = Person.objects.get(pk = randint(1, 500))
                    if not (GroupMember.objects.filter(person = person,
                                                   group = group).exists()):
                        break
                GroupMember.objects.get_or_create(person = person,
                                                  group = group)
