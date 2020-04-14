from django.urls import path
from . import views
from .views import URPDetailView, URPCreateView, ApplicationDetailView, application_create, application_status, view_my_urps, view_applications


urlpatterns = [
    path('', views.home, name='uap-home'),
    path('about/', views.about, name='uap-about'),
    path('application/status', application_status, name='application-status'),
    path('urp/myurp', view_my_urps, name='my-urps'),
    path('urp/<int:pk>', URPDetailView.as_view(), name='urp-detail'),
    path('application/<int:pk>', ApplicationDetailView.as_view(), name='application-detail'),
    path('application/list/<int:pk>', view_applications, name='view-applications'),
    path('urp/new/', URPCreateView.as_view(), name='urp-create'),
    path('urp/<int:pk>/apply/', application_create, name='urp-apply'),
]
