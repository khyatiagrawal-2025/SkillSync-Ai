from django.db import models
from django.contrib.auth.models import User

# 1. Student Model: Stores basic info
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    joining_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.roll_number}"

# 2. Performance Model: To track SkillSync-AI scores
class Performance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.IntegerField()
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject}"