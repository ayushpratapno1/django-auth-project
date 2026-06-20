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
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Choose a codename',
            'first_name': 'Enter first name',
            'last_name': 'Enter last name',
            'email': 'Enter email address',
            'password1': 'Create passphrase',
            'password2': 'Confirm passphrase'
        }

        labels = {
            'username': 'Codename',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Contact Email',
            'password1': 'Security Passphrase',
            'password2': 'Confirm Passphrase',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control auth-input',
                'placeholder': placeholders.get(field_name, '')
            })
            if field_name in labels:
                field.label = labels[field_name]


class ProfileForm(forms.ModelForm):

  class Meta:
    model = Profile

    fields = [
        'profile_picture',
        'bio',
        'division',
        'specialty',
        'territory',
    ]

  def __init__(self, *args, **kwargs):

    super().__init__(*args, **kwargs)

    placeholders = {
        'bio': 'Write your member description...',
        'specialty': 'Strategist, Negotiator, Operations...',
        'territory': 'North Sector, South Sector...'
    }

    labels = {
        'profile_picture': 'Profile Image',
        'bio': 'Member Description',
        'division': 'Division',
        'specialty': 'Specialty',
        'territory': 'Territory',
        'rank': 'Rank',
    }

    for field_name, field in self.fields.items():

        field.widget.attrs.update({
            'class': 'form-control'
        })

        if field_name in placeholders:
            field.widget.attrs.update({
                'placeholder': placeholders[field_name]
            })

        if field_name in labels:
            field.label = labels[field_name]