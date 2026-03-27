from django.shortcuts import render, redirect
from .models import Student

# 1. Login View (SkillSync-AI ka entry point)
def login_view(request):
    return render(request, "accounts/login.html")

# 2. Registration View (Naya student add karne ke liye)
def register_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # Image handle karne ke liye request.FILES ka use hota hai
        image = request.FILES.get('image') 
        
        Student.objects.create(
            name=name, 
            email=email, 
            phone_number=phone,
            student_image=image
        )
        return redirect("login")
        
    return render(request, "accounts/register.html")

# 3. Forgot Password View
def forgot_password_view(request):
    return render(request, "accounts/forgot_password.html")