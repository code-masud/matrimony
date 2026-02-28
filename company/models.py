from django.db import models
from services.uploads import logo_upload_path
from services.validations import image_validation
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class CompanyInfo(models.Model):
    name = models.CharField(max_length=200)
    phone = PhoneNumberField(
        unique=True,
        verbose_name="Phone Number",
        null=True,
    )
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    description = models.TextField(null=True)
    logo = models.ImageField(upload_to=logo_upload_path, validators=[image_validation], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Company Information'