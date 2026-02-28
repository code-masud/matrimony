from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class User(AbstractUser):

    class OnBehalfChoices(models.TextChoices):
        SELF = "self", "Self"
        SON = "son", "Son"
        DAUGHTER = "daughter", "Daughter"
        BROTHER = "brother", "Brother"
        SISTER = "sister", "Sister"
        FRIEND = "friend", "Friend"
        RELATIVE = "relative", "Relative"

    on_behalf = models.CharField(
        max_length=20,
        choices=OnBehalfChoices.choices,
        default=OnBehalfChoices.SELF,
        db_index=True,
        verbose_name="On Behalf Of"
    )

    phone = PhoneNumberField(
        unique=True,
        verbose_name="Phone Number"
    )

    is_verified = models.BooleanField(
        default=False,
        db_index=True
    )

    class Meta:
        ordering = ["-date_joined"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.username} - {self.get_on_behalf_display()}"
    