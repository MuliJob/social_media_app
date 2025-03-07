from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post, Comment, Trend, PostAttachment


class PostAttachmentSerializer(serializers.ModelSerializer):
    """Post attachment serializer"""
    class Meta:
        """CLass Meta"""
        model = PostAttachment
        fields = ('id', 'get_image',)


class PostSerializer(serializers.ModelSerializer):
    """Post serializer"""
    created_by = UserSerializer(read_only=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)
    class Meta:
        """class meta"""
        model = Post
        fields = (
            'id',
            'body',
            'is_private',
            'likes_count',
            'comments_count',
            'created_by',
            'created_at_formatted',
            'attachments',
        )

class CommentSerializer(serializers.ModelSerializer):
    """Comments model serializer"""
    created_by = UserSerializer(read_only=True)

    class Meta:
        """Class meta"""
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at_formatted',)


class PostDetailSerializer(serializers.ModelSerializer):
    """Post details serializer"""
    created_by = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    attachments = PostAttachmentSerializer(read_only=True, many=True)

    class Meta:
        """Class meta"""
        model = Post
        fields = ('id', 'body',
                  'likes_count', 'comments_count',
                  'created_by', 'created_at_formatted',
                  'comments', 'attachments',
                  )


class TrendSerializer(serializers.ModelSerializer):
    """Trends serializers"""
    class Meta:
        """Class meta"""
        model = Trend
        fields = ('id', 'hashtag', 'occurrences',)
