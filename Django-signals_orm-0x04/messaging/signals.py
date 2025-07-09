from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory

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
