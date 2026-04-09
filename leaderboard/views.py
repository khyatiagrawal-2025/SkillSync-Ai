from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.views.decorators.cache import never_cache



@login_required
@never_cache
def leaderboard_view(request):
    
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    # Sabhi users ko XP ke hisaab se rank karo
    all_users = UserProfile.objects.all().order_by('-xp_points')
    
    # Top 3 for special display
    top_3 = all_users[:3]
    
    # Baaki list (Rank 4 se 10 tak)
    remaining_users = all_users[3:10]
    
    # Current logged-in user ki profile
    user_profile = None
    user_rank = 1
    for profile in all_users:
        if profile.user == request.user:
            break
        user_rank += 1
        
    context = {
        'top_3': top_3,
        'remaining_users': remaining_users,
        'user_profile': user_profile,
        'user_rank': user_rank,
    }
    return render(request, 'leaderboard/leaderboard.html', context)