from django.shortcuts import render, redirect
from .models import Student
from django.views.decorators.http import require_POST
from django.contrib.auth.views import LoginView as AuthLoginView
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm


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

# def forgot_password_view(request):
    
#     if request.method == 'POST':
#         name = request.POST.get('user_name')
#         phone_number = request.POST.get('phone_number')
#         email = request.POST.get('user_email')
       
        
#         if name and phone_number.isdigit() and len(phone_number) == 10 and email :
#             data = forgot_password_view(Name=name, 
#                              Email=email,
#                             )
#             data.save()
            
#      # Send confirmation email
#             subject = 'Reset Password Confirmation'
#             message = "Hello ,\n\nYour booking has been successfully received.\n" \
                      
            
#             from_email = settings.DEFAULT_FROM_EMAIL
#             recipient_list = [email]  # The email of the user

#             # Send the confirmation email
#             send_mail(subject, message, from_email, recipient_list)
            
#             return render(request, 'accounts/forgot_password.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/forgot_password.html'
    email_template_name = 'accounts/password_reset_email.txt'   # text version
    html_email_template_name = 'accounts/password_reset_email.html'  # HTML version
    subject_template_name = 'accounts/password_reset_subject.txt'   # ✅ OPTIONAL
    success_url = reverse_lazy('password_reset_done')
    
    def form_valid(self, form):
        self.request.session['reset_email'] = form.cleaned_data['email']
        return super().form_valid(form)


def resend_reset_email(request):
    email = request.session.get('reset_email')

    if email:
        form = PasswordResetForm({'email': email})
        if form.is_valid():
            form.save(
                request=request,
                email_template_name='accounts/password_reset_email.html',
                subject_template_name='accounts/password_reset_subject.txt'
            )

    return redirect('password_reset_done')


def reset_password_view(request):
    return render(request, 'accounts/reset_password.html')

def LogoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')  # Redirect to a page after logout, e.g., the home page