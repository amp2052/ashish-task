from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Notification
from .tasks import send_notification_email


def custom_login(request):
    """
    Custom login view that:
    - Authenticates user
    - If password is wrong, creates a Notification and sends an email asynchronously using Celery
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        # If authentication fails
        if user is None:
            try:
                user_obj = User.objects.get(username=username)
                message = "Someone attempted to log in with the wrong password."
                
                # Save notification in DB
                Notification.objects.create(user=user_obj, message=message)

                # Send async email using Celery
                send_notification_email.delay(
                    subject="Login Failed Alert",
                    message=message,
                    recipient=user_obj.email
                )
            except User.DoesNotExist:
                pass  # username doesn't exist, skip silently

            return render(request, 'app/login.html', {'error': 'Invalid credentials'})

        # Successful login
        login(request, user)
        return redirect('home')  # change 'home' to your dashboard or homepage name

    return render(request, 'app/login.html')
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'app/home.html')
