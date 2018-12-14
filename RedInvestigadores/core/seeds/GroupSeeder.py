from faker import Faker
from core.models import Group, GroupMember, Person
from random import randint

"""
Class to seed groups into the database.

"""

class GroupSeeder(object):
    """
    GroupSeeder is the one who has the capacity of creating N groups
    and inserting each one of them into the database, it can also add
    random individuals as members of this groups.

    """

    def seed(self):
        """
        Creates 200 different groups and inserts them into the database.
        Each of them follows the model a group has:
        * name  - Random company name is given
        * owner - Random person is selected
        """

        faker = Faker()
        for i in range(200):
            name = faker.company()
            owner = Person.objects.get(pk = randint(1, 350))

            Group.objects.get_or_create(name = name,
                                        owner = owner)

    def seed_members(self):
        """
        Creates 200 different group members and inserts them into the database.
        Each of them follows the model a group member has:
        * group  - Group is selected
        * person - Random person is selected

        If the person is already a member of the group then another person is selected.
        Each group has a random number of members.
        """

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
