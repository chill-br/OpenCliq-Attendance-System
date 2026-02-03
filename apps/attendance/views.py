import json
import csv
from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db.models import Sum
from .models import Meeting

# Import your models
from .models import Attendance, Task
from django.contrib.auth import get_user_model
User = get_user_model() # This is the "safe" way to get your User model  # Or use get_user_model()

@login_required
def dashboard(request):
    user = request.user
    today = timezone.now().date()
    
    # --- 1. STATS CALCULATIONS ---
    # Today's Total
    today_logs = Attendance.objects.filter(user=user, date=today, check_out__isnull=False)
    today_seconds = sum((log.check_out - log.check_in).total_seconds() for log in today_logs)
    today_hours = round(today_seconds / 3600, 1)

    # Monthly Total
    current_month = today.month
    monthly_logs = Attendance.objects.filter(user=user, date__month=current_month, check_out__isnull=False)
    monthly_seconds = sum((log.check_out - log.check_in).total_seconds() for log in monthly_logs)
    monthly_hours = int(monthly_seconds // 3600)

    # Avg Check-in
    all_logs = Attendance.objects.filter(user=user).order_by('check_in')
    avg_text = "09:00 AM" 
    if all_logs.exists():
        avg_text = all_logs.first().check_in.strftime("%I:%M %p")

    # --- 2. ATTENDANCE & TEAM LOGIC ---
    logs = Attendance.objects.filter(user=user).order_by('-check_in')[:10]
    active_session = Attendance.objects.filter(user=user, check_out__isnull=True).first()
    online_team = User.objects.filter(is_online=True).exclude(id=user.id)
    offline_team = User.objects.filter(is_online=False).exclude(id=user.id)

    # --- 3. TASK LOGIC ---
    tasks = Task.objects.filter(user=user).order_by('-created_at')

    context = {
        'logs': logs,
        'active_session': active_session,
        'online_team': online_team,
        'offline_team': offline_team,
        'today_hours': today_hours,
        'monthly_hours': monthly_hours,
        'avg_check_in': avg_text,
        'tasks': tasks,
    }

    days = []
    hours_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        days.append(date.strftime('%a'))
        
        # Get all logs for this day
        day_logs = Attendance.objects.filter(user=user, date=date)
        total_seconds = 0
        
        for log in day_logs:
            if log.check_out:
                total_seconds += (log.check_out - log.check_in).total_seconds()
            elif log.date == today:
                # If still checked in today, calculate time up until "now"
                total_seconds += (timezone.now() - log.check_in).total_seconds()
        
        hours_data.append(round(total_seconds / 3600, 1))
    context = {
        # ... your other context variables ...
        'chart_days': json.dumps(days),
        'chart_data': json.dumps(hours_data),
    }

    upcoming_meetings = Meeting.objects.filter(
        start_time__gte=timezone.now()
    ).order_by('start_time')[:3] # Show only the next 3

    context = {
        # ... your other context ...
        'meetings': upcoming_meetings,
    }
    
    return render(request, 'dashboard.html', context)

@login_required
def toggle_attendance(request):
    user = request.user
    now = timezone.now()
    active_session = Attendance.objects.filter(user=user, check_out__isnull=True).first()

    if active_session:
        active_session.check_out = now
        active_session.save()
        user.is_online = False
    else:
        selected_mode = request.POST.get('work_mode', 'OFFICE')
        Attendance.objects.create(
            user=user, 
            check_in=now, 
            date=now.date(),
            work_mode=selected_mode
        )
        user.is_online = True
    
    user.save()
    return redirect('dashboard')

@login_required
def export_attendance(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{request.user.username}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Check In', 'Check Out', 'Work Mode'])
    
    logs = Attendance.objects.filter(user=request.user).order_by('-date')
    for log in logs:
        writer.writerow([log.date, log.check_in, log.check_out, log.work_mode])
        
    return response

# --- TASK API VIEW FUNCTIONS ---

@login_required
def add_task(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_text = data.get('text')
            if task_text:
                task = Task.objects.create(user=request.user, text=task_text)
                return JsonResponse({
                    'id': task.id, 
                    'text': task.text, 
                    'is_completed': task.is_completed
                })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.is_completed = not task.is_completed
        task.save()
        return JsonResponse({'is_completed': task.is_completed})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_task(request, task_id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def toggle_break(request):
    session = Attendance.objects.filter(user=request.user, check_out__isnull=True).first()
    if session:
        # Check if model has these fields before saving
        if hasattr(session, 'on_break'):
            if not session.on_break:
                session.on_break = True
                session.break_start = timezone.now()
            else:
                if session.break_start:
                    duration = timezone.now() - session.break_start
                    session.total_break_time += duration
                session.on_break = False
                session.break_start = None
            session.save()
    return redirect('dashboard')


@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    
    workers = User.objects.all()
    # Path is 'admin/filename.html' because they are inside the admin folder
    return render(request, 'admin/workers_list.html', {'workers': workers})

@login_required
def workers_list(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    workers = User.objects.all()
    return render(request, 'admin/workers_list.html', {'workers': workers})

@login_required
def all_attendance(request):
    if not request.user.is_staff:
        return redirect('dashboard')
    all_logs = Attendance.objects.all().order_by('-date')
    return render(request, 'admin/attendance_logs.html', {'all_logs': all_logs})

@login_required
def edit_worker(request, user_id):
    if not request.user.is_staff:
        return redirect('dashboard')
        
    worker = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        # Get data from the form fields in edit_worker.html
        worker.username = request.POST.get('username')
        worker.email = request.POST.get('email')
        worker.department = request.POST.get('department')
        
        # Update staff status if your template has this checkbox
        worker.is_staff = 'is_staff' in request.POST 
        
        worker.save()
        return redirect('workers-list') # Take us back to the list after saving
        
    return render(request, 'admin/edit_worker.html', {'worker': worker})

from .models import Meeting

@login_required
def create_meeting(request):
    if not request.user.is_staff:
        return redirect('dashboard')
        
    if request.method == "POST":
        # Get data from the form
        title = request.POST.get('title')
        description = request.POST.get('description')
        link = request.POST.get('link')
        start_time = request.POST.get('start_time')
        
        # Create the meeting object
        Meeting.objects.create(
            title=title,
            description=description,
            meeting_link=link,
            start_time=start_time
        )
        return redirect('admin-dashboard')
    
    # This points to: templates/admin/create_meeting.html
    return render(request, 'admin/create_meeting.html')