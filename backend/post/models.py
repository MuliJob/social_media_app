import uuid

from django.conf import settings
from django.db import models
from django.utils.timesince import timesince

from account.models import User


class Like(models.Model):
    """Likes model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

class Comment(models.Model):
    """POst comments"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta:
        """Class meta"""
        ordering = ('created_at',)

    def created_at_formatted(self):
        """Formatted date"""
        return timesince(self.created_at)

class PostAttachment(models.Model):
    """Attaching an image to a post"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)

    def get_image(self):
        """GETTING THE IMAGE FUNCTION"""
        if self.image:
            return settings.WEBSITE_URL + self.image.url
        else:
            return ''

class Post(models.Model):
    """POst model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)

    is_private = models.BooleanField(default=False)

    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    reported_by_users = models.ManyToManyField(User, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    objects = models.Manager()

    class Meta:
        """Class meta"""
        ordering = ('-created_at',)

    def created_at_formatted(self):
        """Humanizing date"""
        return timesince(self.created_at)


class Trend(models.Model):
    """Trend models"""
    hashtag = models.CharField(max_length=255)
    occurrences = models.IntegerField()

    objects = models.Manager()
