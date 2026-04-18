from django.urls import path


from .views import dashboard  # correct name
from . import views

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('progress/', views.progress_dashboard, name='progress'),
    path('settings/', views.settings_view, name='settings'),
    path('skill-advisor/', views.skill_advisor, name='skill_advisor'),
    path('roadmap/<int:roadmap_id>/', views.roadmap_detail, name='roadmap_detail'),
    #path('groq-advisor/', views.ask_groq_advisor, name='groq_advisor')

    
]
