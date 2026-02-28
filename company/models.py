from django.db import models
from services.uploads import logo_upload_path
from services.validations import image_validation
from phonenumber_field.modelfields import PhoneNumber

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200)
    phone = PhoneNumber()
    email = models.EmailField(blank=True, null=True)
    address = models.TextField()
    logo = models.ImageField(upload_to=logo_upload_path, validators=[image_validation], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.name