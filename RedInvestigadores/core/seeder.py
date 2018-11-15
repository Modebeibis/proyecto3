from django_seed import Seed
from core.models import Affiliation, Person, Journal

from random import randint

seeder = Seed.seeder()

## Affiliation Seeder ##

seeder.add_entity(Affiliation, 10, {
    'name': lambda x, seeder = seeder: seeder.faker.company(),
    'super_level': lambda x: None,
    'address': lambda x, seeder = seeder: seeder.faker.address(),
})

seeder.add_entity(Affiliation, 25, {
    'name': lambda x, seeder = seeder: seeder.faker.company(),
    'super_level': lambda x: randint(1, 10),
    'address': lambda x, seeder = seeder: seeder.faker.address(),
})

seeder.add_entity(Affiliation, 35, {
    'name': lambda x, seeder = seeder: seeder.faker.company(),
    'super_level': lambda x: randint(10, 35),
    'address': lambda x, seeder = seeder: seeder.faker.address(),
})

## Person Seeder ##

seeder.add_entity(Person, 500, {
    'first_name': lambda x, seeder = seeder: seeder.faker.first_name(),
    'last_name': lambda x, seeder = seeder: seeder.faker.first_name(),
    'affiliation': lambda x, seeder = seeder: randint(1, 70),
    'email': lambda x, seeder = seeder: seeder.faker.email(),
    'orcid': lambda x, seeder = seeder: seeder.faker.isbn10(),
    'role': lambda x, seeder = seeder: randint(1, 4),
    'state': lambda x, seeder = seeder: randint(1, 29),
})

## Role Seeder ##
### Admin ###
for i in range(25):
    r = randint(1, 350)

    seeder.add_entity(PersonRole, 1, {
        'person': lambda x, r = r: r,
        'role': lambda x: 4,
    })

    seeder.add_entity(Administrator, 1, {
        'person': lambda x, r = r: r,
    })

### Researcher ###
for i in range(350):

    seeder.add_entity(PersonRole, 1, {
        'person': lambda x, i = i: i,
        'role': lambda x: 3,
    })

    seeder.add_entity(Researcher, 1, {
        'person': lambda x, i = i: i,
    })

### Postdoc ###
for i in range(150):
    r = randint(1, 500)

    seeder.add_entity(PersonRole, 1, {
        'person': lambda x, r = r: r,
        'role': lambda x: 2,
    })

    seeder.add_entity(Postdoc, 1, {
        'person': lambda x, r = r: r,
    })
### Student ###
for i in range(351, 501):
    seeder.add_entity(PersonRole, 1, {
        'person': lambda x, i = i: i,
        'role': lambda x: 1,
    })

    seeder.add_entity(Student, 1, {
        'person': lambda x, i = i: i,
    })

#### StudentOf ####
for i in range(351, 501):
    r = randint(1, 350)

    seeder.add_entity(StudentOf, 1, {
        'student': lambda x, i = i: i,
        'tutor': lambda x, r = r: r,
    })

## Grant Seeder ##
seeder.add_entity(Grant, 100, {
    'responsible': lambda x: randint(1, 350),
    'title': lambda x, seeder = seeder: seeder.faker.username(),
    'start_date': lambda x, seeder = seeder: seeder.faker.date_time(),
    'end_date': lambda x, seeder = seeder: seeder.faker.date_time(),
})

## GrantParticipant Seeder ##

seeder.add_entity(Grant, 100, {
    'person': lambda x: randint(1, 500),
    'grant': lambda x: randint(1, 100),
})

## Journal Seeder ##

seeder.add_entity(Journal, 50, {
    'name': lambda x, seeder = seeder: seeder.faker.username(),
    'issn': lambda x, seeder = seeder: seeder.faker.isbn10()
})

## Publication Seeder ##

seeder.add_entity(Publication, 1000, {
    'title': lambda x, seeder = seeder: seeder.faker.sentence(),
    'journal': lambda x, seeder = seeder: randint(1, 50),
    'volume': lambda x, seeder = seeder: randint(1, 200),
    'issue': lambda x, seeder = seeder: seeder.faker.paragraph(),
    'date': lambda x, seeder = seeder: seeder.faker.date(),
    'doi': lambda x, seeder = seeder: seeder.faker.isbn10(),
})

seeder.add_entity(AuthorOf, 1000, {
    'person': lambda x, seeder = seeder: randint(1, 500),
    'publication': lambda x, seeder = seeder: randint(1, 1000),
})

seeder.add_entity(ExternalAuthor, 20, {
    'first_name': lambda x, seeder = seeder: seeder.faker.first_name(),
    'last_name': lambda x, seeder = seeder: seeder.faker.first_name(),
})

seeder.add_entity(AuthorOfExternal, 100, {
    'author': lambda x, seeder = seeder: randint(1, 20),
    'publication': lambda x, seeder = seeder: randint(1, 1000),
})

## Group Seeder ##

seeder.add_entity(Group, 300, {
    'name': lambda x, seeder = seeder: seeder.faker.username(),
    'owner': lambda x, seeder = seeder: randint(1, 500),
})

seeder.add_entity(GroupMember, 50) {
    'group': lambda x, seeder = seeder: randint(1, 300),
    'person': lambda x, seeder = seeder: randint(1, 500),
}

## Petitions ##

### UserPetition ###
seeder.add_entity(UserPetition, 200, {
    'name': lambda x, seeder = seeder: seeder.faker.name(),
    'last_name': lambda x, seeder = seeder: seeder.faker.last_name(),
    'email': lambda x, seeder = seeder: seeder.faker.email(),
})

### AffiliationPetition ###
r = randint(1, 80)
r = r if r <= 70 else None

seeder.add_entity(AffiliationPetition, 200, {
    'name': lambda x, seeder = seeder: seeder.faker.company(),
    'email': lambda x, seeder = seeder: seeder.faker.email(),
    'address': lambda x, seeder = seeder: seeder.faker.address(),
    'id_super_level': lambda x, r = r: r,
})

### PublicationPetition ###
seeder.add_entity(PublicationPetition, 300, {
    'id_researcher': lambda x: randint(1, 350),
    'title': lambda x, seeder = seeder: seeder.faker.sentence(),
    'journal': lambda x, seeder = seeder: randint(1, 50),
    'volume': lambda x, seeder = seeder: randint(1, 200),
    'issue': lambda x, seeder = seeder: seeder.faker.paragraph(),
    'date': lambda x, seeder = seeder: seeder.faker.date(),
    'doi': lambda x, seeder = seeder: seeder.faker.isbn10(),
})

### JournalPetition ###
seeder.add_entity(JournalPetition, 50, {
    'id_researcher': lambda x: randint(1, 350),
    'name': lambda x, seeder = seeder: seeder.faker.username(),
    'issn': lambda x, seeder = seeder: seeder.faker.isbn10()
})

### ExternalAuthorPetition ###
seeder.add_entity(ExternalAuthorPetition, 20, {
    'id_researcher': lambda x: randint(1, 350),
    'first_name': lambda x, seeder = seeder: seeder.faker.first_name(),
    'last_name': lambda x, seeder = seeder: seeder.faker.first_name(),
})

### GroupPetition ###
seeder.add_entity(ExternalAuthorPetition, 150, {
    'id_researcher': lambda x: randint(1, 350),
    'name': lambda x, seeder = seeder: seeder.faker.username(),
})

### GroupAddPetition ###
for i in range(1, 300):
    researcher_owner_id = randint(1, 350)
    person_to_add_id = researcher_owner_id
    while person_to_add_id == researcher_owner_id:
        person_to_add_id = randint(1, 350)

    b = randint(0,1)
    r = randint(1, 300)
    group_id = r if b else None
    r = randint(1, 150)
    petition_group_id = r if not b else None


    seeder.add_entity(GroupAddPetition, 1, {
        'id_researcher_owner': lambda x, id = researcher_owner_id: id,
        'id_person_to_add': lambda x, id = person_to_add_id: id,
        'id_group': lambda x, id = group_id: id,
        'id_petition_group': lambda x, id = petition_group_id: id,
    })

seeder.execute()

print('Your database is now seeded')
