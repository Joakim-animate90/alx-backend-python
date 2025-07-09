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

def get_threaded_messages(message_id):
    """Recursively fetch a message and all its replies"""
    message = Message.objects.filter(pk=message_id).prefetch_related(
        Prefetch('replies', 
            queryset=Message.objects.all().prefetch_related(
                Prefetch('replies', queryset=Message.objects.all())
            )
        )
    ).first()
    return message

@login_required
def get_message_thread(request, message_id):
    """API endpoint to get a message and its full reply thread"""
    message = get_threaded_messages(message_id)
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
