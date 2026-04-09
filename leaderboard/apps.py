from django.apps import AppConfig

class LeaderboardConfig(AppConfig):
    name = 'leaderboard'
    default_auto_field = 'django.db.models.BigAutoField'
    
    def ready(self):
        import leaderboard.signals 