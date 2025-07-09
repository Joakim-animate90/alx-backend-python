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
