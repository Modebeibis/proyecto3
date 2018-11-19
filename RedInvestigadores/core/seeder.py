from core.seeds.AffiliationSeeder import AffiliationSeeder
from core.seeds.PersonSeeder import PersonSeeder
from core.seeds.GrantSeeder import GrantSeeder
from core.seeds.JournalSeeder import JournalSeeder
from core.seeds.PublicationSeeder import PublicationSeeder
from core.seeds.GroupSeeder import GroupSeeder
from core.seeds.PetitionSeeder import PetitionSeeder

print('Seeding Database:')
print('- - - - Seeding Affiliations...')
AffiliationSeeder().seed()
print('- - - - Seeding Persons...')
PersonSeeder().seed()
print('- - - - Seeding Administrators...')
PersonSeeder().seed_admins()
print('- - - - Seeding Researchers...')
PersonSeeder().seed_researchers()
print('- - - - Seeding Postdocs...')
PersonSeeder().seed_postdocs()
print('- - - - Seeding Students...')
PersonSeeder().seed_students()
print('- - - - Seeding relationships between Researchers and Students.')
PersonSeeder().seed_student_of_relationships()
PersonSeeder().fill_person_and_roles()
print('- - - - Now all persons on the DB have a role.')
print('- - - - Seeding Grants')
GrantSeeder().seed()
print('- - - - Seeding Grant participants')
GrantSeeder().seed_participants()
print('- - - - Seeding Journals')
JournalSeeder().seed()
print('- - - - Seeding Publications')
PublicationSeeder().seed()
print('- - - - Seeding Publications authors')
PublicationSeeder().seed_authors()
print('- - - - Seeding External authors')
PublicationSeeder().seed_external_authors()
print('- - - - Seeding Groups')
GroupSeeder().seed()
print('- - - - Seeding Groups members')
GroupSeeder().seed_members()
print('- - - - Seeding User petitions')
PetitionSeeder().seed_user_petitions()
print('- - - - Seeding Affiliation petitions')
PetitionSeeder().seed_affiliation_petitions()
print('- - - - Seeding Journal petitions')
PetitionSeeder().seed_journal_petitions()
print('- - - - Seeding publication petitions')
PetitionSeeder().seed_publication_petitions()
print('- - - - Seeding external author petitions')
PetitionSeeder().seed_external_authors_petitions()
print('- - - - Seeding group petitions')
PetitionSeeder().seed_group_petitions()
print('- - - - Seeding group add members petitions')
PetitionSeeder().seed_group_adding_petitions()
print('Seeding Complete')
