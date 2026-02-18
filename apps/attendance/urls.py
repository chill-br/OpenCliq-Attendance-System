from django.urls import path
from . import views
from .api_views import AttendanceStatsAPI 

app_name = 'attendance'

urlpatterns = [
    # --- Main UI & Dashboard ---
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'), # <--- This name
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # --- Attendance Actions ---
    path('attendance/toggle/', views.toggle_attendance, name='toggle-attendance'),
    path('attendance/break/', views.toggle_break, name='toggle-break'),
    path('attendance/export/', views.export_attendance, name='export-attendance'),
    
    # --- Daily Focus / Tasks ---
    path('task/add/', views.add_task, name='add-task'),
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle-task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete-task'),
    
    # --- Management & Admin (Staff Only) ---
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/meeting/create/', views.create_meeting, name='create-meeting'),
    path('admin/announcement/create/', views.create_announcement, name='create-announcement'),
    
    # --- Profile & Community ---
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),

    # --- APIs ---
    path('api/stats/summary/', AttendanceStatsAPI.as_view(), name='attendance-stats-summary'),
    path('api/attendance/logs/', views.attendance_stats_api, name='attendance-api-logs'),
    path('api/employees/', views.employee_list_api, name='employee-list-api'),
]