from django.db import models
from django.contrib.auth.models import User



# 2. Performance Model: To track SkillSync-AI scores
class Performance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    score = models.IntegerField()
    attendance_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.subject}"
    
class AIQuery(models.Model):
    user_skill = models.CharField(max_length=200)
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.user_skill