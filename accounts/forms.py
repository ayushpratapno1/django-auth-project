from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'profile_picture',
            'bio',
            'github',
            'linkedin'
        ]