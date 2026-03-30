from django.contrib import admin

# Register your models here.
#home page ke liye admin panel me user profile ko register karna zaroori hai taki hum uske data ko manage kar sakein.
#home page models and dashboard page models are not created by me .... first i created them then i deleted them and then i created them again because of some errors but now they are working fine.
from .models import UserProfile

admin.site.register(UserProfile)