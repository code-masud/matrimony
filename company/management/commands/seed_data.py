from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from faker import Faker
import random
import requests
from datetime import date

from profiles.models import (
    AnnualIncomeChoices, EducationChoices, GenderChoices,
    MaritalStatusChoices, MatrimonyProfile, MotherTongueChoices,
    OccupationChoices, PartnerPreference, ReligionChoices, ProfilePhoto
)
from matches.models import InterestRequest, Shortlist
from cities_light.models import Country, City, Region
User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Generate fake users, profiles, preferences, interests, shortlists, and images"

    def handle(self, *args, **kwargs):
        users = []

        def get_choice(choices):
            return random.choice([c[0] for c in choices])

        def get_fake_avatar():
            url = "https://picsum.photos/300"
            response = requests.get(url)
            return ContentFile(response.content, name=f"avatar_{fake.uuid4()}.jpg")

        def get_fake_gallery_image():
            url = "https://picsum.photos/500"
            response = requests.get(url)
            return ContentFile(response.content, name=f"gallery_{fake.uuid4()}.jpg")

        country_instance = Country.objects.order_by('?').first()

        # Create Users + Profiles + Preferences
        for _ in range(50):  # number of users
            user = User.objects.create_user(
                username=fake.unique.user_name(),
                email=fake.unique.email(),
                phone=fake.unique.phone_number(),
                on_behalf="self",
                password="password123"
            )

            # Create MatrimonyProfile
            gender = get_choice(GenderChoices.choices)
            dob = fake.date_of_birth(minimum_age=20, maximum_age=40)
            profile = MatrimonyProfile.objects.create(
                user=user,
                gender=gender,
                date_of_birth=dob,
                height_cm=random.randint(140, 200),
                marital_status=get_choice(MaritalStatusChoices.choices),
                religion=get_choice(ReligionChoices.choices),
                mother_tongue=get_choice(MotherTongueChoices.choices),
                education=get_choice(EducationChoices.choices),
                occupation=get_choice(OccupationChoices.choices),
                annual_income=get_choice(AnnualIncomeChoices.choices),
                country=country_instance,
                state=Region.objects.order_by('?').first(),
                city=City.objects.order_by('?').first(),
                about_me=fake.text(max_nb_chars=120),
                profile_picture=get_fake_avatar()
            )

            # Partner Preference
            min_age = random.randint(20, 30)
            max_age = random.randint(min_age, 40)
            min_height = random.randint(140, 160)
            max_height = random.randint(min_height, 200)

            PartnerPreference.objects.create(
                user=user,
                min_age=min_age,
                max_age=max_age,
                min_height_cm=min_height,
                max_height_cm=max_height,
                religion=get_choice(ReligionChoices.choices),
                marital_status=get_choice(MaritalStatusChoices.choices),
                education=get_choice(EducationChoices.choices),
                occupation=get_choice(OccupationChoices.choices),
                country=country_instance,
                state=Region.objects.order_by('?').first(),
                city=City.objects.order_by('?').first(),
            )

            # Gallery Photos (1-5)
            gallery_count = random.randint(1, 5)
            for _ in range(gallery_count):
                ProfilePhoto.objects.create(
                    user=user,
                    image=get_fake_gallery_image(),
                    is_primary=False
                )

            # Set one primary photo randomly
            photos = ProfilePhoto.objects.filter(user=user)
            if photos.exists():
                primary_photo = random.choice(list(photos))
                primary_photo.is_primary = True
                primary_photo.save()

            users.append(user)

        self.stdout.write(self.style.SUCCESS(
            "✅ Users, profiles, preferences, and images created"))

        # Create Shortlists
        for user in users:
            others = [u for u in users if u != user]
            shortlisted = random.sample(others, k=min(5, len(others)))
            for target in shortlisted:
                Shortlist.objects.get_or_create(
                    user=user,
                    shortlisted_user=target
                )

        self.stdout.write(self.style.SUCCESS("✅ Shortlists created"))

        # Create Interest Requests
        for _ in range(100):
            sender, receiver = random.sample(users, 2)
            InterestRequest.objects.get_or_create(
                sender=sender,
                receiver=receiver,
                defaults={
                    "status": random.choice([
                        InterestRequest.StatusChoices.PENDING,
                        InterestRequest.StatusChoices.ACCEPTED,
                        InterestRequest.StatusChoices.REJECTED,
                    ]),
                    "message": fake.sentence()
                }
            )

        self.stdout.write(self.style.SUCCESS("✅ Interest requests created"))
