from rest_framework import serializers

from account.serializers import UserSerializer

from .models import Conversation, ConversationMessage


class ConversationSerializer(serializers.ModelSerializer):
    """COnversation serializer"""
    users = UserSerializer(read_only=True, many=True)

    class Meta:
        """Class meta"""
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted',)


class ConversationMessageSerializer(serializers.ModelSerializer):
    """Conversation Message serializer"""
    sent_to = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        """Class meta"""
        model = ConversationMessage
        fields = ('id', 'sent_to', 'created_by', 'created_at_formatted', 'body',)


class ConversationDetailSerializer(serializers.ModelSerializer):
    """COnversation detail serializer"""
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:
        """Class detail"""
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages',)
