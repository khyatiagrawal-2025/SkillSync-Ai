from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    user = request.user
    profile = getattr(user, 'profile', None)

    context = {
        'user': user,
        'profile': profile,
    }

    return render(request, 'user_profile/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        # Update user fields
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')

        user.save()

        return redirect('profile')  # after save

    # 👇 IMPORTANT: render page on GET
    return render(request, 'user_profile/edit_profile.html', {
        'user': user
    })


@login_required
def change_password(request):
    return render(request, 'user_profile/change_password.html')