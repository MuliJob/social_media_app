from django.forms import ModelForm

from .models import Post


class PostForm(ModelForm):
    """POst Form"""
    class Meta:
        """Class Meta"""
        model = Post
        fields = ('body',)


# class AttachmentForm(ModelForm):
#     """Attaching file form"""
#     class Meta:
#         """Class meta"""
#         model = PostAttachment
#         fields = ('image',)
