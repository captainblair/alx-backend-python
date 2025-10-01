from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Signal receiver that creates a notification when a new message is created.
    """
    if created:
        # Create a notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance,
            is_read=False
        )


@receiver(pre_save, sender=Message)
def track_message_edits(sender, instance, **kwargs):
    """
    Signal receiver that tracks message edits and saves the previous version.
    """
    if not instance.pk:
        # New message, no edit history to track
        return
        
    try:
        old_instance = Message.objects.get(pk=instance.pk)
        if old_instance.content != instance.content:
            # Message content was edited, save the old version
            MessageHistory.objects.create(
                message=old_instance,
                content=old_instance.content,
                edited_by=instance.sender  # Assuming the sender is the one editing
            )
            instance.edited = True
    except Message.DoesNotExist:
        # Message doesn't exist yet (shouldn't happen in pre_save)
        pass


def ready(self):
    ""
    Import signals to ensure they are registered when the app is ready.
    This method is called in the AppConfig.ready() method.
    """
    # Import signals to register them
    import messaging.signals  # noqa
