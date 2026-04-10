from datetime import date
from django.db import models
from django.conf import settings
from services.uploads import avatar_upload_path, gallery_image_upload_path
from services.validations import image_validation
from cities_light.models import Country, Region, City


class EducationChoices(models.TextChoices):
    # Undergraduate
    BTECH = "btech", "B.Tech / B.E."
    BSC = "bsc", "B.Sc"
    BCOM = "bcom", "B.Com"
    BA = "ba", "B.A."
    BBA = "bba", "B.B.A."
    BCA = "bca", "B.C.A."
    MBBS = "mbbs", "M.B.B.S."
    # Postgraduate
    MTECH = "mtech", "M.Tech / M.E."
    MSC = "msc", "M.Sc"
    MA = "ma", "M.A."
    MBA = "mba", "M.B.A."
    MCA = "mca", "M.C.A."
    MD = "md", "M.D."
    # Doctorate & Others
    PHD = "phd", "Ph.D / Doctorate"
    DIPLOMA = "diploma", "Diploma"
    HIGHER_SECONDARY = "higher_secondary", "12th / Higher Secondary"
    OTHER = "other", "Other"


class OccupationChoices(models.TextChoices):
    # Professional
    SOFTWARE = "software", "Software Engineer / IT Professional"
    ENGINEER = "engineer", "Engineer (Non-IT)"
    DOCTOR = "doctor", "Doctor / Medical Professional"
    TEACHER = "teacher", "Teacher / Professor"
    ACCOUNTANT = "accountant", "Chartered Accountant / Finance"
    MANAGEMENT = "management", "Management / HR Professional"
    # Government & Civil
    GOVT_SERVICE = "govt_service", "Government Employee"
    CIVIL_SERVICES = "civil_services", "IAS / IPS / Civil Services"
    DEFENCE = "defence", "Defence / Military"
    # Business & Creative
    BUSINESS = "business", "Business Owner / Entrepreneur"
    CREATIVE = "creative", "Artist / Designer / Media"
    # General
    PRIVATE_SECTOR = "private", "Private Sector Employee"
    HOMEMAKER = "homemaker", "Homemaker"
    STUDENT = "student", "Student"
    NOT_WORKING = "not_working", "Not Working"
    OTHER = "other", "Other"


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


class AnnualIncomeChoices(models.TextChoices):
    NO_INCOME = "0", "No Income"
    UNDER_1L = "0-1", "Under 1 Lakh"
    L1_TO_3L = "1-3", "1 Lakh - 3 Lakhs"
    L3_TO_5L = "3-5", "3 Lakhs - 5 Lakhs"
    L5_TO_7L = "5-7", "5 Lakhs - 7 Lakhs"
    L7_TO_10L = "7-10", "7 Lakhs - 10 Lakhs"
    L10_TO_15L = "10-15", "10 Lakhs - 15 Lakhs"
    L15_TO_20L = "15-20", "15 Lakhs - 20 Lakhs"
    L20_TO_30L = "20-30", "20 Lakhs - 30 Lakhs"
    L30_TO_50L = "30-50", "30 Lakhs - 50 Lakhs"
    L50_TO_1CR = "50-100", "50 Lakhs - 1 Crore"
    ABOVE_1CR = "100+", "1 Crore & Above"


def get_height_choices():
    choices = []
    for cm in range(121, 245):
        # Convert cm to feet and inches for the label
        total_inches = cm / 2.54
        feet = int(total_inches // 12)
        inches = round(total_inches % 12)

        # Handle rounding overflow (e.g., 5'12" -> 6'0")
        if inches == 12:
            feet += 1
            inches = 0

        label = f"{cm} cm ({feet}'{inches}\")"
        choices.append((cm, label))
    return choices


# Use this in your model
HEIGHT_CHOICES = get_height_choices()


class MotherTongueChoices(models.TextChoices):
    # Primary (Bangladesh/West Bengal)
    BENGALI = "bengali", "Bengali"

    # Common South Asian
    HINDI = "hindi", "Hindi"
    URDU = "urdu", "Urdu"
    PUNJABI = "punjabi", "Punjabi"
    ARABIC = "arabic", "Arabic"
    ENGLISH = "english", "English"

    # Regional (India/Pakistan/Others)
    GUJARATI = "gujarati", "Gujarati"
    KANNADA = "kannada", "Kannada"
    MALAYALAM = "malayalam", "Malayalam"
    MARATHI = "marathi", "Marathi"
    ODIA = "odia", "Odia"
    SINDHI = "sindhi", "Sindhi"
    TAMIL = "tamil", "Tamil"
    TELUGU = "telugu", "Telugu"
    ASSAMESE = "assamese", "Assamese"
    SYLHETI = "sylheti", "Sylheti"
    CHITTAGONIAN = "chittagonian", "Chittagonian"

    # Others
    FRENCH = "french", "French"
    GERMAN = "german", "German"
    SPANISH = "spanish", "Spanish"
    OTHER = "other", "Other"


class MatrimonyProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="matrimony_profile"
    )

    # Basic Info
    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices, db_index=True)
    date_of_birth = models.DateField()
    height_cm = models.PositiveIntegerField(
        choices=get_height_choices(),
        help_text="Height in centimeters",
        db_index=True
    )
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
    mother_tongue = models.CharField(
        max_length=50,
        choices=MotherTongueChoices.choices,
        default=MotherTongueChoices.BENGALI,
        db_index=True
    )

    # Education & Career
    education = models.CharField(
        max_length=50,
        choices=EducationChoices.choices,
        default=EducationChoices.OTHER
    )
    occupation = models.CharField(
        max_length=50,
        choices=OccupationChoices.choices,
        default=OccupationChoices.OTHER
    )
    annual_income = models.CharField(
        max_length=20,
        choices=AnnualIncomeChoices.choices,
        blank=True,
        null=True,
        help_text="Select your annual income range"
    )

    # Location
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)

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

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        not_yet_reached = (today.month, today.day) < (
            self.date_of_birth.month, self.date_of_birth.day)
        return today.year - self.date_of_birth.year - not_yet_reached

    def get_completion_percentage(self):
        required_fields = [
            'gender', 'date_of_birth', 'height_cm', 'marital_status',
            'religion', 'education', 'occupation', 'country',
            'state', 'city', 'about_me', 'profile_picture'
        ]

        filled_count = 0
        for field in required_fields:
            value = getattr(self, field)

            if value not in [None, "", [], {}]:
                filled_count += 1

        return int((filled_count / len(required_fields)) * 100)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["gender", "religion", "city"]),
        ]

    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        percentage = self.get_completion_percentage()

        if percentage >= 100 and self.user.first_name:
            self.is_profile_completed = True
        else:
            self.is_profile_completed = False

        super().save(*args, **kwargs)


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
    min_height_cm = models.PositiveIntegerField(
        choices=get_height_choices(),
        null=True,
        blank=True
    )
    max_height_cm = models.PositiveIntegerField(
        choices=get_height_choices(),
        null=True,
        blank=True
    )

    # Basic Filters
    religion = models.CharField(
        max_length=20,
        choices=ReligionChoices.choices,
        db_index=True
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatusChoices.choices,
        db_index=True
    )

    # Education & Career
    education = models.CharField(
        max_length=50,
        choices=EducationChoices.choices,
        default=EducationChoices.OTHER
    )
    occupation = models.CharField(
        max_length=50,
        choices=OccupationChoices.choices,
        default=OccupationChoices.OTHER
    )

    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(
        Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} Partner Preference"


class ProfilePhoto(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(upload_to=gallery_image_upload_path, validators=[
                              image_validation], blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.user.username} Photo"


class ProfileView(models.Model):
    viewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='views_made'
    )
    viewed = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='views_received'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['viewer', 'viewed']),
            models.Index(fields=['created_at'])
        ]

    def __str__(self):
        return f"{self.viewer} → {self.viewed}"
