from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory

User = get_user_model()


class MessagingModelTests(TestCase):
    def setUp(self):
        # Create test users
        self.sender = User.objects.create_user(
            username='sender',
            email='sender@example.com',
            password='testpass123'
        )
        self.receiver = User.objects.create_user(
            username='receiver',
            email='receiver@example.com',
            password='testpass123'
        )

    def test_create_message(self):
        ""Test creating a new message."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, this is a test message!'
        )
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(str(message), f'Message from {self.sender} to {self.receiver} at {message.timestamp}')

    def test_message_notification_signal(self):
        ""Test that a notification is created when a new message is sent."""
        # Initially no notifications
        self.assertEqual(Notification.objects.count(), 0)

        # Create a message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello, this is a test message!'
        )

        # Check that a notification was created
        self.assertEqual(Notification.objects.count(), 1)
        notification = Notification.objects.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.is_read)

    def test_notification_str_representation(self):
        ""Test the string representation of a notification."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Test message'
        )
        notification = Notification.objects.create(
            user=self.receiver,
            message=message,
            is_read=False
        )
        self.assertEqual(
            str(notification),
            f'Notification for {self.receiver} about message {message.id}'
        )

    def test_message_edit_tracking(self):
        ""Test that message edits are tracked in history."""
        # Create initial message
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Original message'
        )
        
        # Verify no edit history yet
        self.assertEqual(message.edit_history.count(), 0)
        self.assertFalse(message.edited)
        
        # Edit the message
        message.content = 'Updated message'
        message.save()
        
        # Refresh from db
        message.refresh_from_db()
        
        # Verify edit was tracked
        self.assertTrue(message.edited)
        self.assertEqual(message.edit_history.count(), 1)
        
        # Check history entry
        history = message.edit_history.first()
        self.assertEqual(history.content, 'Original message')
        self.assertEqual(history.edited_by, self.sender)
        
        # Edit again
        message.content = 'Final message'
        message.save()
        
        # Verify new history entry
        self.assertEqual(message.edit_history.count(), 2)
        self.assertEqual(message.edit_history.last().content, 'Updated message')

    def test_message_history_str_representation(self):
        ""Test the string representation of message history."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Test message'
        )
        
        # Create history entry
        history = MessageHistory.objects.create(
            message=message,
            content='Old content',
            edited_by=self.sender
        )
        
        self.assertIn(f'Edit of message {message.id} at', str(history))
