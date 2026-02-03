from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('toggle/', views.toggle_attendance, name='toggle-attendance'),
    path('break/', views.toggle_break, name='toggle-break'),
    path('export/', views.export_attendance, name='export-attendance'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/add/', views.add_task, name='add-task'),
    path('task/toggle/<int:task_id>/', views.toggle_task, name='toggle-task'),
    path('task/delete/<int:task_id>/', views.delete_task, name='delete-task'),
    path('management/', views.admin_dashboard, name='admin-dashboard'),
    path('management/workers/', views.workers_list, name='workers-list'),
    path('management/attendance/', views.all_attendance, name='all-attendance'),
    path('management/workers/edit/<int:user_id>/', views.edit_worker, name='edit-worker'),
    path('management/meetings/create/', views.create_meeting, name='create-meeting'),
]