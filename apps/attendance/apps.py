from django.apps import AppConfig


# apps/attendance/apps.py
class AttendanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.attendance'
    label = 'attendance'

