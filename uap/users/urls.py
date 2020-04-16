from django.contrib import admin
from django.urls import path, include
from .views import serve_resume, update_profile

urlpatterns = [
    path('resume/', serve_resume, name='resume'),
    path('profile/update/', update_profile, name='update-profile'),
]