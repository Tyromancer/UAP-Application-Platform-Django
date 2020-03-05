from django.urls import path
from . import views
from .views import URPDetailView, URPCreateView


urlpatterns = [
    path('', views.home, name='uap-home'),
    path('about/', views.about, name='uap-about'),
    path('urp/<int:pk>', URPDetailView.as_view(), name='urp-detail'),
    path('urp/new/', URPCreateView.as_view(), name='urp-create'),
]
