from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

urlpatterns = [
    # 🔐 Auth Routes
    path("login/", views.login_view.as_view(), name="login"),
    path("register/", views.register_view, name="register"),

    path("logout/", views.LogoutView, name="logout"),

    # 🔑 Password Reset Flow
    path("forgot-password/", CustomPasswordResetView.as_view(), name="password_reset"),

    path("password-reset-done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"),
        name="password_reset_done"),
    
    path('resend-email/', views.resend_reset_email, name='resend_email'),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view( template_name="accounts/password_reset_confirm.html"),
        name="password_reset_confirm"),


    path("reset-done/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"),
        name="password_reset_complete"),
    
]