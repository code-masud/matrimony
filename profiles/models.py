from django.db import models
from django.conf import settings
from services.uploads import avatar_upload_path, gallery_image_upload_path
from services.validations import image_validation

# Create your models here.
class MatrimonyProfile(models.Model):

    class GenderChoices(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"

    class MaritalStatusChoices(models.TextChoices):
        NEVER_MARRIED = "never_married", "Never Married"
        DIVORCED = "divorced", "Divorced"
        WIDOWED = "widowed", "Widowed"
        ANNULLED = "annulled", "Annulled"

    class ReligionChoices(models.TextChoices):
        MUSLIM = "muslim", "Muslim"
        HINDU = "hindu", "Hindu"
        CHRISTIAN = "christian", "Christian"
        SIKH = "sikh", "Sikh"
        OTHER = "other", "Other"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matrimony_profile"
    )

    # Basic Info
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, db_index=True)
    date_of_birth = models.DateField()
    height_cm = models.PositiveIntegerField(help_text="Height in centimeters")
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatusChoices.choices,
        db_index=True
    )

    # Religion & Community
    religion = models.CharField(
        max_length=20,
        choices=ReligionChoices.choices,
        db_index=True
    )
    caste = models.CharField(max_length=100, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)

    # Education & Career
    education = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    annual_income = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True
    )

    # Location
    country = models.CharField(max_length=100, db_index=True)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100, db_index=True)

    # About
    about_me = models.TextField(blank=True)

    # Profile Media
    profile_picture = models.ImageField(
        upload_to=avatar_upload_path,
        validators=[image_validation],
        blank=True,
        null=True
    )

    is_profile_completed = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["gender", "religion", "city"]),
        ]

    def __str__(self):
        return f"{self.user.username} Profile"
    

class PartnerPreference(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="partner_preference"
    )

    # Age Preference
    min_age = models.PositiveIntegerField()
    max_age = models.PositiveIntegerField()

    # Height Preference
    min_height_cm = models.PositiveIntegerField(blank=True, null=True)
    max_height_cm = models.PositiveIntegerField(blank=True, null=True)

    # Basic Filters
    religion = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    # Education & Career
    education = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Partner Preference"
    
class ProfilePhoto(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(upload_to=gallery_image_upload_path, validators=[image_validation])
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.user.username} Photo"