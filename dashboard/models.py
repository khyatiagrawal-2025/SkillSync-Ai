from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



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


# 1. User Profile for Core Stats (XP, Level, Streak)
class UserProgressProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="progress_profile")
    total_xp = models.IntegerField(default=0)
    current_level = models.IntegerField(default=1)
    tasks_done = models.IntegerField(default=0)
    current_streak = models.IntegerField(default=0)
    best_streak = models.IntegerField(default=0)
    consistency_pct = models.IntegerField(default=0)
    global_rank = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Progress"

# 2. Skill Mastery Tracker
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100) # e.g., "HTML / CSS"
    icon = models.CharField(max_length=10)  # e.g., "🌐"
    proficiency = models.IntegerField(default=0) # 0 to 100
    level_label = models.CharField(max_length=50) # e.g., "Expert", "Beginner"
    color_class = models.CharField(max_length=20, default="pill-b") # For CSS styling

    def __str__(self):
        return f"{self.name} - {self.proficiency}%"

# 3. Task Management
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    xp_reward = models.IntegerField(default=50)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

# 4. Badge System
class Badge(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10) # e.g., "🏆"
    description = models.TextField()

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="earned_badges")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

# 5. NEW: Saved AI Roadmaps & Insights
class SavedAIRoadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_roadmaps")
    title = models.CharField(max_length=255, default="My AI Roadmap")
    ai_content = models.TextField() # Gemini ka generate kiya hua markdown/HTML
    generated_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True) # Agar current roadmap hai toh True

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    

# Ye AI ka data save karne ke liye table hai
# class AICache(models.Model):
#     prompt_text = models.CharField(max_length=500, unique=True) 
#     ai_response = models.TextField() 
#     created_at = models.DateTimeField(auto_now_add=True) 

#     def __str__(self):
#         return self.prompt_text
    
# ai response ko save karne ke liye table hai
class AICache(models.Model):
    prompt_text = models.CharField(max_length=1500, unique=True) 
    ai_response = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Cache: {self.prompt_text[:30]}..."