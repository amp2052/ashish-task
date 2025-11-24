from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(subject, message, recipient):
    send_mail(
        subject,
        message,
        "amp2052@gmail.com",   # sender
        [recipient],
        fail_silently=False
    )
