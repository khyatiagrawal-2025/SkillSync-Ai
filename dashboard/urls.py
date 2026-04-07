from django.urls import path

from dashboard.models import Student
from .views import dashboard  # correct name
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('progress/', views.progress_view, name='progress'),
    path('settings/', views.settings_view, name='settings'),
]
