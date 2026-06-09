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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Enter username',
            'first_name': 'Enter first name',
            'last_name': 'Enter last name',
            'email': 'Enter email',
            'password1': 'Create password',
            'password2': 'Confirm password'
        }

        for field_name, field in self.fields.items():

            field.widget.attrs.update({
                'class': 'form-control auth-input',
                'placeholder': placeholders.get(field_name, '')
            })


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile

        fields = [
            'profile_picture',
            'bio',
            'github',
            'linkedin'
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        placeholders = {
            'bio': 'Tell us about yourself...',
            'github': 'https://github.com/username',
            'linkedin': 'https://linkedin.com/in/username'
        }

        for field_name, field in self.fields.items():

            field.widget.attrs.update({
                'class': 'form-control'
            })

            if field_name in placeholders:

                field.widget.attrs.update({
                    'placeholder': placeholders[field_name]
                })