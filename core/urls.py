

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as acc_views 

urlpatterns = [
    # 1. Django Default Admin (ONLY ONCE)
    path('admin/', admin.site.urls),
    path('', include('attendance.urls')), 
    #path('attendance/', include('attendance.urls')),
    #path('attendance/', include('attendance.u
    # 2. Django Auth (login/logout)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # 3. Attendance App (ONLY ONCE with namespace)
    # This makes 'attendance:dashboard' work
    path('attendance/', include(('attendance.urls', 'attendance'), namespace='attendance')),
    # 4. Custom Account Views
    path('register/', acc_views.register, name='register'),
    path('profile/', acc_views.profile, name='profile'),

    # 5. Admin Console
    path('admin-console/workers/', acc_views.admin_workers_list, name='admin-workers'),
    path('admin-console/workers/edit/<int:pk>/', acc_views.admin_edit_worker, name='admin-edit-worker'),
    path('admin-console/attendance/', acc_views.admin_attendance_logs, name='admin-attendance-logs'),

] 

# 6. Static and Media Files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)