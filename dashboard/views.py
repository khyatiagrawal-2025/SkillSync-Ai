from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Student
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def dashboard(request):
    # 1. Accounts App se Data: Total Students count
    total_students_count = Student.objects.count()

    # Context mein sabhi data ko ek saath bhejna
    context = {
        'total_students': total_students_count,
        'user': request.user,
        # 'stats': user_stats, # Agar model banaya hai toh
        'page_name': "SkillSync-AI Dashboard"
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