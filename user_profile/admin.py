from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
  
    list_display = ('user', 'phone_number', 'target_role') 
    
    # Search karne ke liye user ke username ya email ka use karein
    search_fields = ('user__username', 'user__email', 'phone_number')
    
    # Optional: Filters add karne ke liye
    list_filter = ('target_role',)