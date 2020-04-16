from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import URPDetailView, URPCreateView, ApplicationDetailView, application_create, application_status, view_my_urps, view_applications, view_and_manage_application


urlpatterns = [
    path('', views.home, name='uap-home'),
    path('about/', views.about, name='uap-about'),
    path('application/status', application_status, name='application-status'),
    path('urp/myurp', view_my_urps, name='my-urps'),
    path('urp/<int:pk>', URPDetailView.as_view(), name='urp-detail'),
    path('application/<int:pk>', ApplicationDetailView.as_view(), name='application-detail'),
    path('application/list/<int:pk>', view_applications, name='view-applications'),
    path('application/manage/<int:pk>', view_and_manage_application, name='manage-application'),
    path('urp/new/', URPCreateView.as_view(), name='urp-create'),
    path('urp/<int:pk>/apply/', application_create, name='urp-apply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)