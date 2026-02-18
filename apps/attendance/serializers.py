# apps/attendance/serializers.py
from rest_framework import serializers
from .models import Attendance
from django.contrib.auth import get_user_model
from rest_framework import serializers


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id','user', 'date', 'check_in', 'check_out','work_mode','latitude', 'longitude']


User = get_user_model()

class EmployeeSerializer(serializers.ModelSerializer):
    # This adds a custom field to show if they are currently clocked in
    current_status = serializers.BooleanField(source='is_online', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'department', 'current_status']
