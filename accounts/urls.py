from django.urls import path
from . import views

urlpatterns = [
    # SkillSync-AI Accounts Routes
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("forget-password/", views.forget_password_view, name="forget_password"),
]