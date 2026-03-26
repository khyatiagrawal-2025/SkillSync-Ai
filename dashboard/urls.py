from django.urls import path
from .views import dashboard_view   # correct name

urlpatterns = [
    path('', dashboard_view, name='dashboard'),
]