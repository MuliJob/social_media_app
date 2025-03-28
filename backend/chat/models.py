import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User


class Conversation(models.Model):
    """COnversation model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def modified_at_formatted(self):
        """Modified date"""
        return timesince(self.created_at)


class ConversationMessage(models.Model):
    """Conversation model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation,
                                     related_name='messages',
                                     on_delete=models.CASCADE)
    body = models.TextField()
    sent_to = models.ForeignKey(User,
                                related_name='received_messages',
                                on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   related_name='sent_messages',
                                   on_delete=models.CASCADE)

    objects = models.Manager()

    def created_at_formatted(self):
        """Formatted date"""
        return timesince(self.created_at)
