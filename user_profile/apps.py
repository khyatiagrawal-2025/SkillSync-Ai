from django.apps import AppConfig


class UserProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_profile'

    def ready(self):
        # Signals ko import karna yahan zaroori hai
        import user_profile.signals