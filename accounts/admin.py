

from django.contrib import admin
from .models import Student, Attendance, PasswordResetToken # Apne models import karein

# Student model ko register karein
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at') # Panel mein ye columns dikhenge
    search_fields = ('name', 'email') # Search bar enable ho jayega

# Attendance model ko register karein
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', ) # Panel mein ye columns dikhenge
    search_fields = ('student__name',) # Search bar enable ho jayega
    
    
    
 # PasswordResetToken model ko register karein
@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token')
    search_fields = ('user__username', 'token')