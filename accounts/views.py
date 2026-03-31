from django.shortcuts import render, redirect
from .models import Student
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy


class login_view(AuthLoginView):
    template_name = 'accounts/login.html'
    def get_success_url(self):
        # Check if the user is an admin
        if self.request.user.is_staff:
            return reverse_lazy('admin:index')  # Redirects to the Django admin panel
        return reverse_lazy('dashboard')  # Redirects to the home page if not an admin   

def register_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, form.errors)
            
    else:
        form = CustomUserForm()
     
    return render(request, 'accounts/register.html', {'form': form})

def forgot_password_view(request):
    return render(request, 'forgot_password.html')