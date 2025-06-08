from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access messages.
    - Only authenticated users can access the API.
    - Only participants in a conversation can send, view, update, and delete messages.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        if not request.user or not request.user.is_authenticated:
            return False

        # For ConversationViewSet, allow all authenticated users to list/retrieve conversations
        if view.basename == 'conversation':
            return True

        # For MessageViewSet, defer to has_object_permission for detail views
        return True

    def has_object_permission(self, request, view, obj):
        # Only allow participants of the conversation to access the message/conversation
        user = request.user

        # For ConversationViewSet, check if user is a participant
        if view.basename == 'conversation':
            return obj.participants.filter(user=user).exists()

        # For MessageViewSet, check if user is a participant in the related conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants.filter(user=user).exists()

        return False
