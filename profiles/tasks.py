from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()


@shared_task
def send_profile_view_email(viewed_id, viewer_id):
    viewed = User.objects.get(id=viewed_id)
    viewer = User.objects.get(id=viewer_id)

    send_mail(
        subject="Someone viewed your profile 👀",
        message=f"{viewer.get_full_name()} viewed your profile.",
        from_email="no-reply@example.com",
        recipient_list=[viewed.email],
        fail_silently=True,
    )
