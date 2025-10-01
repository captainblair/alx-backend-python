from django.db import models
from django.db.models import Q


class UnreadMessagesManager(models.Manager):
    """
    Custom manager for Message model to handle unread messages.
    Optimized to fetch only necessary fields.
    """
    
    def get_queryset(self):
        """Base queryset that only selects related sender and receiver."""
        return super().get_queryset().select_related('sender', 'receiver')
    
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user.
        Uses only() to fetch only necessary fields.
        """
        return self.get_queryset().filter(
            receiver=user,
            is_read=False
        ).only(
            'id', 'content', 'timestamp', 'sender_id', 'receiver_id', 'parent_message_id'
        )
    
    def unread_count(self, user):
        """Returns count of unread messages for a user."""
        return self.unread_for_user(user).count()
    
    def mark_as_read(self, message_ids, user):
        """Mark specific messages as read for a user."""
        return self.filter(
            id__in=message_ids,
            receiver=user,
            is_read=False
        ).update(is_read=True)


class MessageQuerySet(models.QuerySet):
    """Custom QuerySet for Message model with chainable filters."""
    
    def unread(self):
        """Filter only unread messages."""
        return self.filter(is_read=False)
    
    def for_user(self, user):
        """Filter messages for a specific user (either sender or receiver)."""
        return self.filter(Q(sender=user) | Q(receiver=user))
    
    def in_thread(self, thread_id):
        """Filter messages in a specific thread."""
        return self.filter(Q(pk=thread_id) | Q(parent_message_id=thread_id))
