from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def dashboard(request):
    # 1. Current logged-in user ko hi student maan rahe hain
    student = request.user 
    
    # 2. Total registered users count
    total_students = User.objects.count()

    context = {
        'total_students': total_students,
        'student': student, # Ab ye sahi hai
        'user': request.user
    }
    
    return render(request, "dashboard/dashboard.html", context)

def roadmap_view(request):
    return render(request, 'dashboard/roadmap.html')

@login_required
def progress_view(request):
    return render(request, 'dashboard/progress.html')

@login_required
def settings_view(request):
    return render(request, "dashboard/settings.html")