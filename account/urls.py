from email.mime import image
from unicodedata import name
from django.urls import path
from . import views


app_name = 'account'

urlpatterns = [
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('profile/edit/', views.profile_edit, name="profile_edit"),
]
