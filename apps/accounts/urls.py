from django.urls import path
from . import views

urlpatterns = [
    # Profile & Auth
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    
    # Admin Console
    path('admin-console/workers/', views.admin_workers_list, name='admin-workers'),
    path('admin-console/workers/edit/<int:pk>/', views.admin_edit_worker, name='admin-edit-worker'),
    path('admin-console/attendance/', views.admin_attendance_logs, name='admin-attendance-logs'),
]