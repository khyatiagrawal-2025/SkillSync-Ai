from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    dob = models.DateField(null=True, blank=True)
    college = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    def __str__(self):
        return self.user.username