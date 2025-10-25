from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_notification_email(to_email, message):
    send_mail(
        'Notification Alert',
        message,
        'amp2052@gmail.com',   # replace with your sender email
        [to_email],
        fail_silently=False,
    )
