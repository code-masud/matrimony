from celery import shared_task
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.db.models import Count
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import ProfileView


@shared_task
def send_daily_profile_views():
    print("Running scheduled task...")

    for item in ProfileView.objects.all():
        print(f"Check views for {item}")


@shared_task
def send_profile_view_digest():
    print("Running scheduled task...")

    since = timezone.now() - timedelta(hours=1)

    views = (
        ProfileView.objects
        .filter(created_at__gte=since)
        .values('viewed__email', 'viewed__id')
        .annotate(total_views=Count('id'))
    )

    for item in views:
        email = item['viewed__email']
        total_views = item['total_views']

        context = {
            'total_views': total_views
        }

        html_content = render_to_string(
            'emails/profile_view_digest.html',
            context
        )

        text_content = f"You have got {total_views} new profile views."

        msg = EmailMultiAlternatives(
            subject='Profile Views Update',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
