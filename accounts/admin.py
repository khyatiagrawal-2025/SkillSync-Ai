

from django.contrib import admin
from .models import  Attendance, PasswordResetToken # Apne models import karein



# Attendance model ko register karein
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status' ) # Panel mein ye columns dikhenge
    
    
    
    
 # PasswordResetToken model ko register karein
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    search_fields = ('user__username', 'token')