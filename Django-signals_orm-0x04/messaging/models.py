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
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        help_text='Reference to the message this is a reply to, if any.'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    thread_updated = models.DateTimeField(
        auto_now=True,
        help_text='Updated when a new reply is added to the thread.'
    )

    class Meta:
        ordering = ['-thread_updated', 'timestamp']
        indexes = [
            models.Index(fields=['receiver', 'is_read']),
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['parent_message']),  # For filtering replies
            models.Index(fields=['thread_updated']),  # For sorting threads
        ]
        
    def save(self, *args, **kwargs):
        """Override save to update thread_updated on parent message when replying."""
        if self.parent_message:
            # Update the parent's thread_updated when a new reply is added
            Message.objects.filter(pk=self.parent_message.pk).update(
                thread_updated=timezone.now()
            )
        super().save(*args, **kwargs)
        
    def get_thread(self, depth=0, max_depth=10):
        """
        Recursively fetch the entire thread of messages.
        
        Args:
            depth: Current recursion depth (used internally)
            max_depth: Maximum depth to prevent infinite recursion
            
        Returns:
            dict: Message with nested replies
        """
        if depth > max_depth:
            return None
            
        return {
            'id': self.id,
            'sender': self.sender.username,
            'receiver': self.receiver.username,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'edited': self.edited,
            'is_read': self.is_read,
            'replies': [
                reply.get_thread(depth + 1, max_depth)
                for reply in self.replies.all().select_related('sender', 'receiver')
            ]
        }

    def get_root(self):
        """
        Get the root message of the thread.
        Uses iterative approach to avoid recursion depth issues.
        """
        current = self
        while current.parent_message:
            current = current.parent_message
        return current
    
    def get_descendants(self, include_self=False):
        """
        Get all descendant messages of this message.
        Uses a non-recursive approach to avoid recursion depth issues.
        """
        from django.db.models import Q
        
        # Start with direct replies
        descendants = list(self.replies.all())
        if include_self:
            result = [self] + descendants
        else:
            result = descendants
        
        # Get all nested replies using a single query
        if descendants:
            # Build a query to get all descendants
            query = Q(pk__in=[m.pk for m in descendants])
            
            # Get all replies to these messages
            level = self.replies.all()
            while level.exists():
                level_pks = list(level.values_list('pk', flat=True))
                next_level = Message.objects.filter(parent_message_id__in=level_pks)
                if next_level.exists():
                    query |= Q(pk__in=list(next_level.values_list('pk', flat=True)))
                    result.extend(next_level)
                level = next_level
        
        return result
    
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
