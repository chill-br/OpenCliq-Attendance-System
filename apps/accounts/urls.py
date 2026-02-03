from django.urls import path
from . import views

urlpatterns = [
    # Worker Admin Pages
    path('admin-console/workers/', views.admin_workers_list, name='admin-workers'),
    path('admin-console/workers/edit/<int:pk>/', views.admin_edit_worker, name='admin-edit-worker'),
    
    # Profile Pages
    path('profile/', views.profile_view, name='profile'),
]