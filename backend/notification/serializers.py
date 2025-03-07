from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer"""
    class Meta:
        """CLass meta"""
        model = Notification
        fields = ('id', 'body', 'type_of_notification', 'post_id', 'created_for_id')
