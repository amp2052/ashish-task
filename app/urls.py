from django.urls import path
from . import views
from .views import custom_login, home
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.custom_login, name='login'),
    path('home/', home, name='home'),
    path('logout/', views.logout_user, name='logout'),
]
