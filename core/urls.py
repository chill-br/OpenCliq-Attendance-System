from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Import from accounts directly
from accounts import views as acc_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Django Auth (login/logout/password reset)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    path('admin/', admin.site.urls),
    # If you want to use namespaces, include it like this:
    path('attendance/', include('attendance.urls', namespace='attendance')),
    # Custom Account Views
    path('register/', acc_views.register, name='register'),
    path('profile/', acc_views.profile, name='profile'),

    # Admin Console
    path('admin-console/workers/', acc_views.admin_workers_list, name='admin-workers'),
    path('admin-console/workers/edit/<int:pk>/', acc_views.admin_edit_worker, name='admin-edit-worker'),
    path('admin-console/attendance/', acc_views.admin_attendance_logs, name='admin-attendance-logs'),

    # Attendance App
    path('', include('attendance.urls')), 
    path('attendance/', include('attendance.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)