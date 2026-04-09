from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)

    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    college = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    TARGET_ROLE_CHOICES = [
        ('backend', 'Backend Developer'),
        ('frontend', 'Frontend Developer'),
        ('fullstack', 'Full Stack Developer'),
        ('ml', 'ML Engineer'),
        ('devops', 'DevOps Engineer'),
    ]
    target_role = models.CharField(max_length=20, choices=TARGET_ROLE_CHOICES, blank=True)
    
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    
    
    def __str__(self):
        return self.user.username