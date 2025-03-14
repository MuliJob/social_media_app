from django.forms import ModelForm

from .models import Post, PostAttachment


class PostForm(ModelForm):
    """POst Form"""
    class Meta:
        """Class Meta"""
        model = Post
        fields = ('body', 'is_private',)


class AttachmentForm(ModelForm):
    """Attaching file form"""
    class Meta:
        """Class meta"""
        model = PostAttachment
        fields = ('image',)
