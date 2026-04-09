from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Student
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def dashboard(request):
    # 1. Accounts App se Data: Total Students count
    student = Student.objects.get(user=request.user)
    total_students = Student.objects.count()

    context = {
        'total_students': total_students,
        'student': student,
        'user': request.user
    }
    
    # Dashboard template ko render karna
    return render(request, "dashboard/dashboard.html", context)

def roadmap_view(request):
    return render(request, 'dashboard/roadmap.html')

@login_required
def progress_view(request):
    return render(request, 'dashboard/progress.html')

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")