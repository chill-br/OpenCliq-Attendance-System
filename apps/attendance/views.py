import json, math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from datetime import timedelta, date, datetime
from django.db.models import Sum
from django.views.decorators.http import require_POST
from .models import Attendance, Task, Meeting, Announcement, TeamPost
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .serializers import AttendanceSerializer, EmployeeSerializer

User = get_user_model()

# --- HELPER FUNCTIONS ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

# --- MAIN UI ---
@login_required
def dashboard(request):
    user = request.user
    today = timezone.localdate()
    start_of_month = today.replace(day=1)
    
    # 1. Attendance Data
    logs = Attendance.objects.filter(user=user).order_by('-date', '-check_in')[:10]
    active_session = Attendance.objects.filter(user=user, check_out__isnull=True).last()
    
    # 2. Stats Calculation
    all_attendance = Attendance.objects.filter(user=user)
    
    # Calculate Today's Hours
    today_logs = all_attendance.filter(date=today)
    today_hours_list = [log.get_duration_hours() for log in today_logs if log.check_out]
    today_hours = round(sum(today_hours_list), 2) if today_hours_list else 0
    
    # Calculate Monthly Hours
    monthly_logs = all_attendance.filter(date__gte=start_of_month)
    monthly_hours = sum([float(log.get_duration_hours() or 0) for log in monthly_logs if log.check_out])

    # 3. Tasks & Meetings
    tasks = Task.objects.filter(user=user, created_at__date=today)
    meetings = Meeting.objects.filter(start_time__date=today).order_by('start_time')
    
    # 4. Team Status
    online_team = User.objects.filter(is_online=True).exclude(id=user.id)
    is_currently_online = active_session is not None

    if user.is_online != is_currently_online:
        user.is_online = is_currently_online
        user.save(update_fields=['is_online'])

    # 5. Chart Data (Last 7 days)
    chart_days, chart_data = [], []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        chart_days.append(day.strftime('%a'))
        day_log = Attendance.objects.filter(user=user, date=day)
        hours = sum([float(l.get_duration_hours() or 0) for l in day_log if l.check_out])
        chart_data.append(hours)
    
    # Team Blog Post Handling
    if request.method == "POST" and 'post_content' in request.POST:
        content = request.POST.get('post_content')
        image = request.FILES.get('post_image') 
        
        if content:
            TeamPost.objects.create(
                author=request.user,
                content=content,
                image=image,
                is_announcement=request.user.is_staff 
            )
            return redirect('attendance:dashboard') 

    posts = TeamPost.objects.select_related('author').all().order_by('-created_at')[:10]

    context = {
        'logs': logs,
        'active_session': active_session,
        'tasks': tasks,
        'meetings': meetings,
        'online_team': online_team,
        'chart_days': chart_days,
        'chart_data': chart_data,
        'today_hours': round(today_hours, 1),
        'monthly_hours': round(monthly_hours, 1),
        'avg_check_in': "09:00", 
        'is_online': is_currently_online,
        'posts': posts,
    }
    return render(request, 'dashboard.html', context)

# --- ATTENDANCE ACTIONS ---
@login_required
def toggle_attendance(request):
    if request.method == 'POST':
        user = request.user
        now_local = timezone.localtime()
        today = now_local.date()

        attendance = Attendance.objects.filter(user=user, date=today).first()

        if attendance and not attendance.check_out:
            attendance.check_out = now_local
            attendance.save()
            
            if hasattr(user, 'is_online'):
                user.is_online = False
                user.save(update_fields=['is_online'])
                
            messages.success(request, "Checked out successfully!")
            return redirect('attendance:dashboard')

        elif attendance and attendance.check_out:
            messages.warning(request, "You have already completed your shift for today.")
            return redirect('attendance:dashboard')

        else:
            mode = request.POST.get('work_mode', 'OFFICE').upper()
            lat_raw = request.POST.get('latitude', '0')
            lng_raw = request.POST.get('longitude', '0')

            try:
                lat = float(lat_raw) if lat_raw and lat_raw != '0' else 0.0
                lng = float(lng_raw) if lng_raw and lng_raw != '0' else 0.0
            except ValueError:
                lat, lng = 0.0, 0.0

            if mode == 'OFFICE':
                office_lat, office_lng = 12.9716, 77.5946 
                if lat == 0.0:
                    messages.error(request, "Location access is required for Office mode.")
                    return redirect('attendance:dashboard')

                dist = calculate_distance(lat, lng, office_lat, office_lng)
                if dist > 20000: # 20km limit
                    messages.error(request, f"Too far from office ({int(dist)}m).")
                    return redirect('attendance:dashboard')

            Attendance.objects.update_or_create(
                user=user, 
                date=today,
                defaults={
                    'check_in': now_local,
                    'work_mode': mode,
                    'latitude': lat,
                    'longitude': lng
                }
            )

            if hasattr(user, 'is_online'):
                user.is_online = True
                user.save(update_fields=['is_online'])

            messages.success(request, f"Checked in via {mode}!")
            
    return redirect('attendance:dashboard')

@login_required
def toggle_break(request):
    att = Attendance.objects.filter(user=request.user, check_out__isnull=True).last()
    if not att:
        return JsonResponse({'error': 'Not checked in'}, status=400)
    
    now = timezone.now()
    if not att.on_break:
        att.on_break, att.break_start = True, now
        att.break_type = request.POST.get('break_type', 'SHORT')
    else:
        if att.break_start:
            att.total_break_time += (now - att.break_start)
        att.on_break, att.break_start, att.break_type = False, None, None
    att.save()
    return JsonResponse({'status': 'success', 'on_break': att.on_break})

@login_required
@require_POST
def add_task(request):
    data = json.loads(request.body)
    task = Task.objects.create(user=request.user, text=data.get('text'))
    return JsonResponse({'status': 'success', 'id': task.id, 'text': task.text})

@login_required
@require_POST
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return JsonResponse({'status': 'success', 'is_completed': task.is_completed})

@login_required
@require_POST
def delete_task(request, task_id):
    Task.objects.filter(id=task_id, user=request.user).delete()
    return JsonResponse({'status': 'success'})

@staff_member_required
def admin_dashboard(request):
    return render(request, 'admin/workers_list.html', {'workers': User.objects.all()})

@staff_member_required
def create_meeting(request):
    if request.method == 'POST':
        Meeting.objects.create(
            created_by=request.user,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            meeting_link=request.POST.get('link'),
            start_time=request.POST.get('start_time')
        )
        messages.success(request, "Meeting scheduled successfully!")
        return redirect('attendance:dashboard') 

    return render(request, 'admin/create_meeting.html')

@staff_member_required
def create_announcement(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            Announcement.objects.create(
                title=data.get('title'), 
                content=data.get('content'), 
                author=request.user
            )
            return JsonResponse({"status": "success", "message": "Announcement posted"}, status=201)
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({"error": "Invalid data format"}, status=400)
            
    return JsonResponse({"error": "Invalid method"}, status=405)

@login_required
def export_attendance(request):
    messages.info(request, "Export feature coming soon!")
    return redirect('attendance:dashboard')

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        avatar = request.FILES.get('avatar')
        if avatar:
            user.avatar = avatar 
        
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('attendance:dashboard')

    return render(request, 'registration/profile.html', {'user': user})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def attendance_stats_api(request):
    logs = Attendance.objects.filter(user=request.user).order_by('-check_in')[:10]
    serializer = AttendanceSerializer(logs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def employee_list_api(request):
    serializer = EmployeeSerializer(User.objects.all(), many=True)
    return Response(serializer.data)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(TeamPost, id=post_id)
    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    else:
        messages.error(request, "You do not have permission to delete this post.")
        
    return redirect('attendance:dashboard')