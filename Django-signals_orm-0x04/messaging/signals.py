from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

@receiver(pre_save, sender=Message)
def capture_message_history(sender, instance, **kwargs):
    if instance.pk:  # Only for existing messages being updated
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:  # Only if content changed
            MessageHistory.objects.create(
                message=instance,
                content=old_message.content
            )
            instance.edited = True
            instance.edited_at = timezone.now()

@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
            Notification.objects.create(
                user=instance.receiver,
                message=instance
            )

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    """Clean up all user-related data when a user is deleted"""
    # Delete all messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for the user
    Notification.objects.filter(user=instance).delete()
    
    # MessageHistory is automatically deleted via CASCADE from Message
