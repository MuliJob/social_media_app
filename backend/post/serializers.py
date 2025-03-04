from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """Post serializer"""
    class Meta:
        """class meta"""
        model = Post
        fields = (
            'id',
            'body',
            'created_at',
            'created_by'
        )
