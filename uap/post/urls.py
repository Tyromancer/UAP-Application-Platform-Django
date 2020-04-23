from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import urp_create_view, urp_update_view, application_detail_view, application_create, application_status, view_my_urps, view_active_applications, view_and_manage_application, view_accepted_applications, view_rejected_applications, urp_detail_view


urlpatterns = [
    path('', views.home, name='uap-home'),
    path('about/', views.about, name='uap-about'),
    path('application/status', application_status, name='application-status'),
    path('urp/myurp', view_my_urps, name='my-urps'),
    path('urp/<int:pk>', urp_detail_view, name='urp-detail'),
    path('urp/update/<int:pk>', urp_update_view, name='urp-update'),
    path('application/<int:pk>', application_detail_view, name='application-detail'),
    path('application/active/<int:pk>', view_active_applications, name='view-applications'),
    path('application/accepted/<int:pk>', view_accepted_applications, name='view-accepted-applications'),
    path('application/rejected/<int:pk>', view_rejected_applications, name='view-rejected-applications'),
    path('application/manage/<int:pk>', view_and_manage_application, name='manage-application'),
    path('urp/new/', urp_create_view, name='urp-create'),
    path('urp/<int:pk>/apply/', application_create, name='urp-apply'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)