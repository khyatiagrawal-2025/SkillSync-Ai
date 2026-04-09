from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import  EditProfileForm
from django.contrib import messages
from .models import Profile

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
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            # Save profile
            profile = form.save(commit=False)

            # Save user fields manually
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name  = form.cleaned_data['last_name']
            user.username   = form.cleaned_data['username']
            user.email      = form.cleaned_data['email']
            user.save()

            profile.save()

            # Password change (optional)
            current = request.POST.get('current_password')
            new     = request.POST.get('new_password')
            confirm = request.POST.get('confirm_password')

            if current and new and confirm:
                if user.check_password(current):
                    if new == confirm:
                        user.set_password(new)
                        user.save()
                        from django.contrib.auth import update_session_auth_hash
                        update_session_auth_hash(request, user)
                    else:
                        messages.error(request, "Passwords do not match")
                        return redirect('edit_profile')
                else:
                    messages.error(request, "Current password incorrect")
                    return redirect('edit_profile')

            messages.success(request, "Profile updated successfully")
            return redirect('edit_profile')

    else:
        form = EditProfileForm(instance=request.user.profile)

        # Pre-fill user data
        form.fields['first_name'].initial = request.user.first_name
        form.fields['last_name'].initial  = request.user.last_name
        form.fields['username'].initial   = request.user.username
        form.fields['email'].initial      = request.user.email

    return render(request, 'user_profile/edit_profile.html', {'form': form})
# @login_required
# def edit_profile(request):
#     user = request.user

#     if request.method == 'POST':
#         # Update user fields
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.username = request.POST.get('username')
#         user.email = request.POST.get('email')

#         user.save()

#         return redirect('profile')  # after save

#     # 👇 IMPORTANT: render page on GET
#     return render(request, 'user_profile/edit_profile.html', {
#         'user': user
#     })


@login_required
def change_password(request):
    return render(request, 'user_profile/change_password.html')