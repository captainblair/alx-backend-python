from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification


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


def ready(self):
    ""
    Import signals to ensure they are registered when the app is ready.
    This method is called in the AppConfig.ready() method.
    """
    # Import signals to register them
    import messaging.signals  # noqa
