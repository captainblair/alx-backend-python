from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification

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
