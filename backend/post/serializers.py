from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """Post serializer"""
    created_by = UserSerializer(read_only=True)
    class Meta:
        """class meta"""
        model = Post
        fields = (
            'id',
            'body',
            'likes_count',
            'created_by',
            'created_at_formatted'
        )
