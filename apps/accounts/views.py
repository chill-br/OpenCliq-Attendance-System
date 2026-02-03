from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login
from django.contrib import messages
from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect  # Add redirect here
from django.contrib.auth.decorators import login_required  # THIS WAS MISSING
from django.contrib import messages
from .forms import ProfileUpdateForm, SignUpForm
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404
from .models import User # Ensure this is your custom User model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import User 
from .forms import AdminWorkerEditForm
from apps.attendance.models import Attendance

def register(request):
    if request.method == 'POST':
        # request.FILES is required for image uploads!
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
    workers = User.objects.all().order_by('department', 'username')
    return render(request, 'admin/workers_list.html', {'workers': workers})

@user_passes_test(lambda u: u.is_superuser)
def admin_edit_worker(request, pk):
    worker = get_object_or_404(User, pk=pk)
    # You can reuse your ProfileUpdateForm here or create a new AdminUserForm
    if request.method == 'POST':
        # Logic to save updated worker info
        pass
    return render(request, 'admin/edit_worker.html', {'worker': worker})




@user_passes_test(lambda u: u.is_superuser)
def admin_workers_list(request):
    workers = User.objects.all().order_by('username')
    return render(request, 'admin/workers_list.html', {'workers': workers})

@user_passes_test(lambda u: u.is_superuser)
def admin_edit_worker(request, pk):
    worker = get_object_or_404(User, pk=pk)
    # For now, just a placeholder redirect
    return render(request, 'admin/edit_worker.html', {'worker': worker})

def profile_view(request):
    return render(request, 'profile.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_edit_worker(request, pk):
    worker = get_object_or_404(User, pk=pk)
    # For now, let's just render a simple page or redirect back
    return render(request, 'admin/edit_worker.html', {'worker': worker})



@user_passes_test(lambda u: u.is_superuser)
def admin_edit_worker(request, pk):
    worker = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = AdminWorkerEditForm(request.POST, instance=worker)
        if form.is_valid():
            form.save()
            return redirect('admin-workers') # Go back to the list
    else:
        form = AdminWorkerEditForm(instance=worker)
    
    return render(request, 'admin/edit_worker.html', {'form': form, 'worker': worker})

@user_passes_test(lambda u: u.is_superuser)
def admin_workers_list(request):
    workers = User.objects.all().order_by('username')
    
    # Logic for the new stats cards
    online_count = User.objects.filter(is_online=True).count()
    # Note: For break_count, you'll need to filter the Attendance model
    from attendance.models import Attendance
    break_count = Attendance.objects.filter(check_out__isnull=True, on_break=True).count()

    return render(request, 'admin/workers_list.html', {
        'workers': workers,
        'online_count': online_count,
        'break_count': break_count
    })

from apps.attendance.models import Attendance # Ensure the import works as discussed

@user_passes_test(lambda u: u.is_superuser)
def admin_attendance_logs(request):
    # Fetch all logs from all users, most recent first
    all_logs = Attendance.objects.all().order_by('-date', '-check_in')
    return render(request, 'admin/attendance_logs.html', {'all_logs': all_logs})

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

from django.db.models import Sum, F, ExpressionWrapper, DurationField
from django.utils import timezone
from apps.attendance.models import Attendance

@user_passes_test(lambda u: u.is_superuser)
def admin_workers_list(request):
    workers = User.objects.all().order_by('username')
    
    # Calculate Total Monthly Hours for the whole company
    current_month = timezone.now().month
    monthly_logs = Attendance.objects.filter(
        date__month=current_month, 
        check_out__isnull=False
    )

    # Use ExpressionWrapper to handle the time math
    total_duration = monthly_logs.annotate(
        duration=F('check_out') - F('check_in')
    ).aggregate(total=Sum('duration'))['total']

    # Convert duration to total hours (handling None cases)
    total_hours = total_duration.total_seconds() // 3600 if total_duration else 0
    # Add these counts
    office_count = Attendance.objects.filter(check_out__isnull=True, work_mode='OFFICE').count()
    remote_count = Attendance.objects.filter(check_out__isnull=True, work_mode='REMOTE').count()

    return render(request, 'admin/workers_list.html', {
        'workers': workers,
        'total_monthly_hours': total_hours,
        'office_count': office_count,
        'remote_count': remote_count,
        # ... your other existing context ...
    })