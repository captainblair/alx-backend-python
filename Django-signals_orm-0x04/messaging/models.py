from django.db import models
from django.conf import settings
from django.utils import timezone

class Message(models.Model):
    """
    Model representing a message between users.
    """
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'is_read']),
            models.Index(fields=['sender', 'receiver']),
        ]

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.timestamp}'


class Notification(models.Model):
    """
    Model representing a notification for a user about a new message.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
        ]

    def __str__(self):
        return f'Notification for {self.user} about message {self.message.id}'


class MessageHistory(models.Model):
    """
    Model to store the edit history of messages.
    """
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='edit_history'
    )
    content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='message_edits'
    )

    class Meta:
        ordering = ['-edited_at']
        verbose_name_plural = 'Message history'
        indexes = [
            models.Index(fields=['message', 'edited_at']),
        ]

    def __str__(self):
        return f'Edit of message {self.message.id} at {self.edited_at}'
