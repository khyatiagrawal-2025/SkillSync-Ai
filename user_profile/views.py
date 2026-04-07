from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user

    # Safe access (error avoid karne ke liye)
    profile = getattr(user, 'profile', None)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'user_profile/profile.html', context)