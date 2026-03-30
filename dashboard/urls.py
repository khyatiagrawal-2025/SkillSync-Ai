from django.urls import path

from dashboard.models import Student
from .views import dashboard  # correct name

urlpatterns = [
    path('', dashboard, name='dashboard'),
]