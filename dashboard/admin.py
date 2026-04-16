from django.contrib import admin
from .models import  Performance
from .models import UserProgressProfile, UserSkill, Task, UserBadge, SavedAIRoadmap


admin.site.register(Performance)
admin.site.register(UserProgressProfile)
admin.site.register(UserSkill)
admin.site.register(Task)
admin.site.register(UserBadge)
@admin.register(SavedAIRoadmap)
class SavedAIRoadmapAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'generated_at', 'is_active')
    search_fields = ('title', 'user__username')
