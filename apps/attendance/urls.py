from django.urls import path
from . import views
from .api_views import AttendanceStatsAPI 

app_name = 'attendance'

urlpatterns = [
    # --- 1. Main UI & User Dashboard ---
    path('', views.dashboard, name='dashboard'), # Primary entry
    path('dashboard/', views.dashboard),          # Alias for dashboard (no name to avoid conflict)

    # --- 2. Management & Staff Console (Staff Only) ---
    # We use 'staff/' to stay completely away from Django's built-in /admin/
    path('staff/', views.admin_dashboard, name='admin_dashboard'),
    #path('dashboard/', views.dashboard_view, name='admin_dashboard'),
    #path('staff/', views.admin_dashboard, name='admin_dashboard'),
    path('staff/meeting/create/', views.create_meeting, name='create_meeting'),
    path('staff/announcement/create/', views.create_announcement, name='create-announcement'),
    path('staff/meeting/create/', views.create_meeting, name='create_meeting'),
    
    # Aliases for Management (keeping your existing URL structures active)
    path('management/', views.admin_dashboard), 
    path('management-panel/', views.admin_dashboard),
    path('management/meeting/create/', views.create_meeting),

    # --- 3. Attendance Actions ---
    path('attendance/toggle/', views.toggle_attendance, name='toggle-attendance'),
    path('attendance/break/', views.toggle_break, name='toggle-break'),
    path('attendance/export/', views.export_attendance, name='export-attendance'),
    
    
    # --- 4. Daily Focus / Tasks ---
    path('meeting/create/', views.create_meeting, name='create_meeting'), # Ensure underscore
    path('task/add/', views.add_task, name='add-task'), # Matches dashboard JS
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle-task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    
    # --- 5. Profile & Community ---
    path('profile/edit/', views.profile_edit, name='profile-edit'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),

    # --- 6. APIs ---
    path('api/stats/summary/', AttendanceStatsAPI.as_view(), name='attendance-stats-summary'),
    path('api/attendance/logs/', views.attendance_stats_api, name='attendance-api-logs'),
    path('api/employees/', views.employee_list_api, name='employee-list-api'),
]