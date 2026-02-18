from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F
from django.utils import timezone

# Local imports
from .models import User 
from .forms import SignUpForm, ProfileUpdateForm, AdminWorkerEditForm

# Import from the other app (using the direct name)
from attendance.models import Attendance 

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def admin_workers_list(request):
    workers = User.objects.all().order_by('username')
    
    # Dashboard Stats
    online_count = User.objects.filter(is_online=True).count()
    office_count = Attendance.objects.filter(check_out__isnull=True, work_mode='OFFICE').count()
    remote_count = Attendance.objects.filter(check_out__isnull=True, work_mode='REMOTE').count()
    
    # Monthly Hours Logic
    current_month = timezone.now().month
    monthly_logs = Attendance.objects.filter(date__month=current_month, check_out__isnull=False)
    
    total_duration = monthly_logs.annotate(
        duration=F('check_out') - F('check_in')
    ).aggregate(total=Sum('duration'))['total']
    
    total_hours = total_duration.total_seconds() // 3600 if total_duration else 0

    return render(request, 'admin/workers_list.html', {
        'workers': workers,
        'online_count': online_count,
        'office_count': office_count,
        'remote_count': remote_count,
        'total_monthly_hours': total_hours,
    })

@user_passes_test(lambda u: u.is_superuser)
def admin_edit_worker(request, pk):
    worker = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminWorkerEditForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            messages.success(request, f"Worker {worker.username} updated.")
            return redirect('admin-workers')
    else:
        form = AdminWorkerEditForm(instance=worker)
    return render(request, 'admin/edit_worker.html', {'form': form, 'worker': worker})

@user_passes_test(lambda u: u.is_superuser)
def admin_attendance_logs(request):
    query = request.GET.get('q')
    date_filter = request.GET.get('date')
    
    logs = Attendance.objects.all().order_by('-date', '-check_in')

    if query:
        logs = logs.filter(user__username__icontains=query)
    if date_filter:
        logs = logs.filter(date=date_filter)

    return render(request, 'admin/attendance_logs.html', {
        'all_logs': logs,
        'query': query,
        'date_filter': date_filter
    })