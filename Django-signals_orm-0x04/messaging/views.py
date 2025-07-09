from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q, Prefetch
from .models import Message, MessageHistory
import json
from django.db.models import Prefetch
from django.core import serializers

def get_threaded_messages(message_id, user):
    """Recursively fetch a message and all its replies with optimized queries"""
    # Base query with:
    # 1. select_related to optimize sender/receiver foreign keys (1 query per level)
    # 2. prefetch_related with Prefetch to optimize nested replies
    # 3. Q filter to ensure user can only access their messages
    message = (
        Message.objects
        .filter(
            Q(sender=user) | Q(receiver=user),  # Ensure user is sender or receiver
            pk=message_id  # Get specific message
        )
        .select_related('sender', 'receiver')  # Optimize sender/receiver lookups
        .prefetch_related(
            Prefetch('replies', 
                queryset=Message.objects
                    .select_related('sender', 'receiver')  # Optimize reply sender/receiver
                    .prefetch_related(
                        Prefetch('replies', 
                            queryset=Message.objects.select_related('sender', 'receiver')
                        )
                    )
            )
        )
        .first()
    )
    return message

@login_required
def get_message_thread(request, message_id):
    """API endpoint to get a message and its full reply thread"""
    message = get_threaded_messages(message_id, request.user)
    if not message:
        return JsonResponse({'error': 'Message not found'}, status=404)
    
    def build_thread(msg):
        return {
            'id': msg.id,
            'sender': msg.sender.username,
            'receiver': msg.receiver.username,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat(),
            'replies': [build_thread(reply) for reply in msg.replies.all()]
        }
    
    return JsonResponse(build_thread(message))

@cache_page(60)
@login_required
def unread_messages(request):
    """
    Get unread messages with optimized queries
    """
    messages = Message.unread.unread_for_user(request.user).only(
        'id', 
        'content',
        'timestamp',
        'edited',
        'last_edited_at',
        'sender__username',
        'last_edited_by__username'
    ).select_related(
        'sender',
        'last_edited_by'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related(
            'sender', 'receiver'
        ))
    )
    
    return JsonResponse({
        'unread_messages': [{
            'id': msg.id,
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat(),
            'edited': msg.edited,
            'last_edited_by': msg.last_edited_by.username if msg.last_edited_by else None,
            'last_edited_at': msg.last_edited_at.isoformat() if msg.last_edited_at else None,
            'reply_count': msg.replies.count()
        } for msg in messages]
    })
@login_required
@require_http_methods(["DELETE"])
def delete_user(request):
    """
    Delete user account and return success response
    """
    user = request.user
    Message.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).delete()
    user.delete()
    return JsonResponse({
        'status': 'success',
        'message': 'User account deleted successfully'
    })
