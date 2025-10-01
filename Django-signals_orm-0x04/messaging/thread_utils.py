from django.db import models
from django.db.models import Prefetch, Q
from django.utils import timezone
from typing import List, Dict, Optional

from .models import Message


def get_threaded_messages(
    user_id: int,
    other_user_id: Optional[int] = None,
    max_depth: int = 10
) -> List[Dict]:
    """
    Fetch all threads for a user, optionally filtered by another user.
    
    Args:
        user_id: ID of the user to fetch threads for
        other_user_id: Optional ID of another user to filter threads
        max_depth: Maximum depth of nested replies to fetch
        
    Returns:
        List of thread root messages with nested replies
    """
    # Base query to get all messages involving the user
    base_query = Q(sender_id=user_id) | Q(receiver_id=user_id)
    if other_user_id:
        base_query &= (Q(sender_id=other_user_id) | Q(receiver_id=other_user_id))
    
    # Prefetch related data to optimize queries
    message_prefetch = Prefetch(
        'replies',
        queryset=Message.objects.select_related('sender', 'receiver')
                              .order_by('timestamp')
    )
    
    # Get all root messages (no parent) involving the user
    root_messages = (
        Message.objects
        .filter(base_query, parent_message__isnull=True)
        .select_related('sender', 'receiver')
        .prefetch_related(message_prefetch)
        .order_by('-thread_updated')
    )
    
    # Convert to nested dictionary structure
    return [build_thread_dict(msg, max_depth) for msg in root_messages]


def build_thread_dict(message: Message, max_depth: int, current_depth: int = 0) -> Dict:
    """
    Recursively build a dictionary representation of a message thread.
    
    Args:
        message: The message to convert to a dict
        max_depth: Maximum depth of nested replies to include
        current_depth: Current recursion depth
        
    Returns:
        Dictionary representation of the message and its replies
    """
    if current_depth > max_depth:
        return None
        
    # Build the base message dictionary
    message_dict = {
        'id': message.id,
        'sender': {
            'id': message.sender.id,
            'username': message.sender.username,
            'email': message.sender.email,
        },
        'receiver': {
            'id': message.receiver.id,
            'username': message.receiver.username,
            'email': message.receiver.email,
        },
        'content': message.content,
        'timestamp': message.timestamp.isoformat(),
        'edited': message.edited,
        'is_read': message.is_read,
        'thread_updated': message.thread_updated.isoformat(),
        'replies': []
    }
    
    # Recursively add replies
    for reply in message.replies.all():
        reply_dict = build_thread_dict(reply, max_depth, current_depth + 1)
        if reply_dict:
            message_dict['replies'].append(reply_dict)
    
    return message_dict


def get_conversation_threads(
    user_id: int,
    other_user_id: int,
    message_id: Optional[int] = None
) -> Dict:
    """
    Get a specific conversation thread between two users.
    
    Args:
        user_id: ID of the current user
        other_user_id: ID of the other user in the conversation
        message_id: Optional specific message ID to get the thread for
        
    Returns:
        Dictionary containing the thread structure
    """
    try:
        if message_id:
            # Get a specific thread by message ID
            message = (
                Message.objects
                .select_related('sender', 'receiver')
                .prefetch_related('replies')
                .get(
                    Q(id=message_id) &
                    (Q(sender_id=user_id) | Q(receiver_id=user_id)) &
                    (Q(sender_id=other_user_id) | Q(receiver_id=other_user_id))
                )
            )
            # If this is a reply, get the root message
            while message.parent_message:
                message = message.parent_message
            return build_thread_dict(message, max_depth=10)
        else:
            # Get all threads between these users
            threads = get_threaded_messages(user_id, other_user_id)
            return {'threads': threads}
    except Message.DoesNotExist:
        return {'error': 'Thread not found or access denied'}
