from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from SpamCaller.models.models import RegisteredProfile, Contact, ContactsProfilesMapping
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Populate the database with random sample data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Users and RegisteredProfiles
        users=[]
        for _ in range(10):
            phone_number = ''.join(filter(str.isdigit, fake.phone_number()))
            user = User.objects.create_user(
                username=fake.user_name(),
                password='password',
            )
            users.append(user)
            Registered_Profile=RegisteredProfile.objects.create(
                user=user,
                phone=int(phone_number),
                spam=fake.boolean(),
                email=fake.email()
            )
            
        # Create Contacts
        for _ in range(50):
            phone_number = ''.join(filter(str.isdigit, fake.phone_number()))
            contact = Contact.objects.create(
                name=fake.name(),
                phone=int(phone_number),
                spam=fake.boolean(),
                email=fake.email() if fake.boolean() else None
            )
            random_user = random.choice(users)
            ContactsProfilesMapping.objects.create(
                    profile=random_user,
                    contact=contact
                )

        self.stdout.write(self.style.SUCCESS('Database populated with random sample data successfully'))
