from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving conversations.
    Supports filtering by participant user_id.
    """
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants__user_id']

class MessageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for listing and retrieving messages.
    Supports filtering by conversation and sender.
    """
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation__conversation_id', 'sender__user_id', 'recipient__user_id']
