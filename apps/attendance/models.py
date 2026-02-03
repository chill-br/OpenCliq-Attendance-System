from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import models
from django.conf import settings
from apps.accounts.models import User

class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    check_in = models.DateTimeField(default=timezone.now)
    check_out = models.DateTimeField(null=True, blank=True)
    date = models.DateField(default=timezone.now)

    # Break Logic
    on_break = models.BooleanField(default=False)
    break_start = models.DateTimeField(null=True, blank=True)
    total_break_time = models.DurationField(default=timezone.timedelta(0))

    WORK_MODES = [
        ('OFFICE', 'In-Office'),
        ('REMOTE', 'Remote/WFH'),
        ('FIELD', 'Field Work'),
    ]
    work_mode = models.CharField(max_length=10, choices=WORK_MODES, default='OFFICE')

    def __str__(self):
        return f"{self.user.username} - {self.date}"

    @property
    def get_duration(self):
        if self.check_in and self.check_out:
            duration = (self.check_out - self.check_in) - self.total_break_time
            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "In Progress"

  # Add this

    
from django.db import models
from django.conf import settings # Import this instead

class Task(models.Model):
    # This string reference breaks the circular dependency
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Meeting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    meeting_link = models.URLField(blank=True)
    start_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title