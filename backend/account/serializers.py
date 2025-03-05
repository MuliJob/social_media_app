from rest_framework import serializers

from .models import User, FriendshipRequest

class UserSerializer(serializers.ModelSerializer):
    """Post serializer"""
    class Meta:
        """class meta"""
        model = User
        fields = (
            'id',
            'name',
            'email',
            'friends_count',
            'posts_count',
            'get_avatar',
        )

class FriendshipRequestSerializer(serializers.ModelSerializer):
    """Friendship request serializer"""
    created_by = UserSerializer(read_only=True)

    class Meta:
        """Class Meta"""
        model = FriendshipRequest
        fields = ('id', 'created_by',)
