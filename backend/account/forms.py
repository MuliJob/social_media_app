from django.contrib.auth.forms import UserCreationForm

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
