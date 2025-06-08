from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Serializes user_id, username, email, first_name, last_name, phone_number, and is_active fields.
    """
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'is_active',
        ]


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    Serializes message_id, sender, recipient, conversation, message_body, and sent_at fields.
    Includes nested sender and recipient user details.
    """
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'recipient',
            'conversation',
            'message_body',
            'sent_at',
        ]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.

    Serializes conversation_id, participants, created_at, and nested messages.
    Includes nested participants and messages.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]
