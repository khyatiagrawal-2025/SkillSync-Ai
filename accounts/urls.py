from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # SkillSync-AI Accounts Routes
    path("login/", views.login_view.as_view(), name="login"),
    path("register/", views.register_view, name="register"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]


