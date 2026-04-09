from django import forms
from django.contrib.auth.models import User
from .models import Profile

class EditProfileForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = [
            'avatar', 'bio', 'date_of_birth', 'phone',
            'college', 'target_role',
            'github', 'linkedin', 'portfolio', 'twitter'
        ]