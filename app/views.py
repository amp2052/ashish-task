from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification
from .tasks import send_notification_email



def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            try:
                user_obj = User.objects.get(username=username)
                message = "Someone attempted to log into your account with the wrong password."

                Notification.objects.create(user=user_obj, message=message)

                if user_obj.email:
                    send_notification_email.delay(
                        "Login Failed Alert",    # positional arg 1
                        message,                 # positional arg 2
                        user_obj.email           # positional arg 3
                    )

            except User.DoesNotExist:
                pass

            return render(request, 'app/login.html', {'error': 'Invalid credentials'})

        login(request, user)
        return redirect('home')

    return render(request, 'app/login.html')



@login_required
def home(request):
    return render(request, 'app/home.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def notifications(request):
    qs = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'app/notifications.html', {"notifications": qs})



