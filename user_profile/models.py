from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
     # SkillSync-AI Student Profile
    # 🔗 LINK WITH DJANGO USER
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(blank=True)
    skills = models.TextField(blank=True)

# Image field (SkillSync-AI ke liye zaroori hai)
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='default.jpg', null=True)
    date_of_birth = models.DateField(null=True, blank=True) 
    
    TARGET_ROLE_CHOICES = [
        ('backend', 'Backend Developer'),
        ('frontend', 'Frontend Developer'),
        ('fullstack', 'Full Stack Developer'),
        ('ml', 'ML Engineer'),
        ('devops', 'DevOps Engineer'),
    ]
    target_role = models.CharField(max_length=20, choices=TARGET_ROLE_CHOICES, blank=True)
    
    college = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    portfolio = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"