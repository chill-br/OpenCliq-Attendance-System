from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.accounts import views as acc_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('register/', acc_views.register, name='register'),
    path('profile/', acc_views.profile, name='profile'),

    path('admin-console/workers/', acc_views.admin_workers_list, name='admin-workers'),
    path('admin-console/workers/edit/<int:pk>/', acc_views.admin_edit_worker, name='admin-edit-worker'),
    path('admin-console/attendance/', acc_views.admin_attendance_logs, name='admin-attendance-logs'),

    # FIXED: Corrected spelling from 'appps' to 'apps'
    path('', include('apps.attendance.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)