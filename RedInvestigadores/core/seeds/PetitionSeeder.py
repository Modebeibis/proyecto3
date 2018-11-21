from faker import Faker
from core.models import Affiliation, Researcher, Journal, Person, Group
from core.models import UserPetition, AffiliationPetition, GroupPetition, GroupAddPetition
from core.models import PublicationPetition, JournalPetition, ExternalAuthorPetition
from random import randint

class PetitionSeeder(object):
    def seed_user_petitions(self):
        faker = Faker()

        for i in range(100):
            name = faker.name()
            last_name = faker.last_name()
            email = faker.email()

            UserPetition.objects.get_or_create(name = name,
                                               last_name = last_name,
                                               email = email)
    def seed_affiliation_petitions(self):
        faker = Faker()

        for i in range(80):
            name = faker.name()
            email = faker.email()
            address = faker.address()
            r = randint(1, 10)
            if (r < 3):
                id_super_level = None
            else:
                id_super_level = Affiliation.objects.get(pk = randint(1, 70))

            AffiliationPetition.objects.get_or_create(name = name,
                                                      email = email,
                                                      address = address,
                                                      id_super_level = id_super_level)

    def seed_journal_petitions(self):
        faker = Faker()

        for i in range(60):
            id_researcher = Researcher.objects.get(pk = randint(1, 350))
            name = faker.name()
            issn = faker.isbn10()

            JournalPetition.objects.get_or_create(id_researcher = id_researcher,
                                                  name = name,
                                                  issn = issn)

    def seed_publication_petitions(self):
        faker = Faker()

        for i in range(300):
            id_researcher = Researcher.objects.get(pk = randint(1, 350))
            title = faker.sentence()
            journal = Journal.objects.get(pk = randint(1, 50))
            volume = randint(1, 20)
            issue = randint(1, 100)
            date = faker.date()
            doi = faker.isbn10()

            PublicationPetition.objects.get_or_create(id_researcher = id_researcher,
                                                      title = title,
                                                      journal = journal,
                                                      volume = volume,
                                                      issue = issue,
                                                      date = date,
                                                      doi = doi)

    def seed_external_authors_petitions(self):
        faker = Faker()

        for i in range(30):
            id_researcher = Researcher.objects.get(pk = randint(1, 350))
            first_name = faker.first_name()
            last_name = faker.last_name()

            ExternalAuthorPetition.objects.get_or_create(id_researcher = id_researcher,
                                                         first_name = first_name,
                                                         last_name = last_name)

    def seed_group_petitions(self):
        faker = Faker()

        for i in range(80):
            id_researcher = Researcher.objects.get(pk = randint(1, 350))
            name = faker.company()

            GroupPetition.objects.get_or_create(id_researcher = id_researcher,
                                                name = name)

    def seed_group_adding_petitions(self):
        for i in range(1, 300):
            id_researcher_owner = Researcher.objects.get(pk = randint(1, 350))
            id_person_to_add = Person.objects.get(pk = randint(1, 500))

            b = randint(0,1)

            if (b):
                r = randint(1, 200)
                id_group = Group.objects.get(pk = r)
                id_petition_group = None
            else:
                r = randint(1, 80)
                id_petition_group = GroupPetition.objects.get(pk = r)
                id_group = None

            GroupAddPetition.objects.get_or_create(id_researcher_owner = id_researcher_owner,
                                                   id_person_to_add = id_person_to_add,
                                                   id_group = id_group,
                                                   id_petition_group = id_petition_group)
