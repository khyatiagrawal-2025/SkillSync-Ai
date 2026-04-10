from django.db import models
import uuid
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    # Ensure yahan field ka naam 'user' hai
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        # Yahan check karein ki 'self.user' hi likha ho
        return f"{self.user.username} - {self.date}"
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.user.username}"
