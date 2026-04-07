from django.db import models
import uuid
from django.contrib.auth.models import User
class Student(models.Model):
    # SkillSync-AI Student Profile
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    # Image field (SkillSync-AI ke liye zaroori hai)
    student_image = models.ImageField(upload_to='student_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    # Student ke saath relationship
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])
    
    def __str__(self):
        return f"{self.student.name} - {self.date} ({self.status})"
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.username}"
