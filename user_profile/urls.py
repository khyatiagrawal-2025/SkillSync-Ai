from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.profile_view, name='profile'),
   path('change-password/', views.change_password, name='change_password'),
   path('edit-profile/', views.edit_profile, name='edit_profile'),
]