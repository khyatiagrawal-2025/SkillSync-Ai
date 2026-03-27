from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    xp_points = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    track_name = models.CharField(max_length=100, default="Backend Dev")
    location = models.CharField(max_length=50, blank=True) 
    profile_pic = models.ImageField(upload_to='profiles/', null=True, blank=True)
    
    # Change calculation (Previous rank vs Current rank)
    previous_rank = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['-xp_points'] # Highest XP first