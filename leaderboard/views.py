from django.shortcuts import render

from .models import UserProfile
from django.db.models import F

def leaderboard(request):
    # Sabhi users ko XP ke hisaab se rank karo
    all_users = UserProfile.objects.all().order_by('-xp_points')
    
    # Top 3 for special display
    top_3 = all_users[:3]
    
    # Baaki list (Rank 4 se 10 tak)
    remaining_users = all_users[3:10]
    
    # Current logged-in user ki profile
    user_profile = None
    user_rank = 0
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
        # Rank nikalne ke liye
        user_rank = list(all_users).index(user_profile) + 1

    context = {
        'top_3': top_3,
        'remaining_users': remaining_users,
        'user_profile': user_profile,
        'user_rank': user_rank,
    }
    return render(request, 'leaderboard/leaderboard.html', context)