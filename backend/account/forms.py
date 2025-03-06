from django.contrib.auth.forms import UserCreationForm
from django import forms

from .models import User

class SignupForm(UserCreationForm):
    """Signup Form"""
    class Meta:
        """Class meta"""
        model = User
        fields = (
            'name',
            'email',
            'password1',
            'password2'
        )


class ProfileForm(forms.ModelForm):
    """Updating user profile form"""
    class Meta:
        """Class meta"""
        model = User
        fields = ('email', 'name', 'avatar',)
