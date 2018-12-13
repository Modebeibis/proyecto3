from core.seeds.AffiliationSeeder import AffiliationSeeder
from core.seeds.PersonSeeder import PersonSeeder
from core.seeds.GrantSeeder import GrantSeeder
from core.seeds.JournalSeeder import JournalSeeder
from core.seeds.PublicationSeeder import PublicationSeeder
from core.seeds.GroupSeeder import GroupSeeder

print('Seeding Database:')
print('- - - - Seeding Affiliations...')
AffiliationSeeder().seed()
print('- - - - Seeding Persons...')
PersonSeeder().seed()
print('- - - - Seeding Administrators...')
PersonSeeder().seed_admins()
# As all persons are now researchers by default then the following code lines are commented
# print('- - - - Seeding Researchers...')
# PersonSeeder().seed_researchers()
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
print('Seeding Complete')
