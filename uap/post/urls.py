from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='uap-home'),
    path('about/', views.about, name='uap-about')
]
