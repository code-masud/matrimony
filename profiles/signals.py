from django.db.models.signals import pre_save, post_delete
from django.core.files.storage import default_storage
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from .models import ProfilePhoto, MatrimonyProfile
from accounts.models import User


def delete_file(filename):
    if not filename:
        return

    if default_storage.exists(filename):
        default_storage.delete(filename)


@receiver(pre_save, sender=MatrimonyProfile)
def on_change_remove_profile_picture(sender, instance, **kwargs):
    if not instance.id:
        return

    profile = get_object_or_404(MatrimonyProfile, pk=instance.id)

    if profile.profile_picture and profile.profile_picture != instance.profile_picture:
        delete_file(profile.profile_picture.name)


@receiver(pre_save, sender=ProfilePhoto)
def on_change_remove_old_gallery_image(sender, instance, **kwargs):
    if not instance.pk:
        # New object, nothing to clean up
        return

    try:
        old_instance = ProfilePhoto.objects.get(pk=instance.pk)
    except ProfilePhoto.DoesNotExist:
        return

    # If the image has changed, delete the old file
    if old_instance.image and old_instance.image != instance.image:
        delete_file(old_instance.image.name)
