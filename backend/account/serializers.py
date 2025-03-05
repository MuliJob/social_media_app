from rest_framework import serializers

from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Post serializer"""
    class Meta:
        """class meta"""
        model = User
        fields = (
            'id',
            'name',
            'email',
        )
