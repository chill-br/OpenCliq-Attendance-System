from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

# 1. ATTENDANCE MODEL
class Attendance(models.Model):
    # Core Fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    work_mode = models.CharField(max_length=20, default='OFFICE')

    # Break Logic
    on_break = models.BooleanField(default=False)
    break_type = models.CharField(
        max_length=20, 
        choices=[('SHORT', 'Short Break'), ('LUNCH', 'Lunch Break')], 
        null=True, 
        blank=True
    )
    break_start = models.DateTimeField(null=True, blank=True)
    total_break_time = models.DurationField(default=timedelta(0))

    # Location / Geofencing
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    is_at_office = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Attendance Logs"
        unique_together = ['user', 'date'] 

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.work_mode})"

    @property
    def get_duration(self):
        """Returns a string formatted duration (e.g., '8h 30m')"""
        if self.check_in and self.check_out:
            duration = (self.check_out - self.check_in) - self.total_break_time
            total_seconds = int(duration.total_seconds())
            if total_seconds < 0: 
                return "0h 0m"
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "Active"

    def get_duration_hours(self):
        """
        FIX FOR ATTRIBUTE ERROR: 
        This is the method your view (line 44) is looking for.
        """
        if self.check_in and self.check_out:
            duration = (self.check_out - self.check_in) - self.total_break_time
            # Return as float for math operations in the view
            return round(max(0, duration.total_seconds() / 3600), 2)
        return 0.0

    def get_total_hours(self):
        """Alias for get_duration_hours to support existing logic if any"""
        return self.get_duration_hours()

# 2. ANNOUNCEMENT MODEL
class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

# 3. TASK MODEL
class Task(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.text[:20]}... ({self.user.username})"

# 4. MEETING MODEL
class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    meeting_link = models.URLField(blank=True)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return self.title