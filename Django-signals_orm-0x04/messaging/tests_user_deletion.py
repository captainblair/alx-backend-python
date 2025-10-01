from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Message, Notification, MessageHistory

User = get_user_model()

class UserDeletionTests(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
        # Create messages between users
        self.message1 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello from user1 to user2'
        )
        
        self.message2 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Reply from user2 to user1'
        )
        
        # Create some notifications
        Notification.objects.create(
            user=self.user1,
            message=self.message2,
            is_read=False
        )
        
        Notification.objects.create(
            user=self.user2,
            message=self.message1,
            is_read=True
        )
        
        # Create some message history
        self.message1.content = 'Updated message content'
        self.message1.save()
        
        # Create a test client
        self.client = Client()
        
    def test_user_deletion_cleanup(self):
        ""Test that user deletion cleans up all related data."""
        # Verify data exists before deletion
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 1)
        self.assertEqual(Message.objects.filter(receiver=self.user1).count(), 1)
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 1)
        self.assertEqual(MessageHistory.objects.filter(edited_by=self.user1).count(), 1)
        
        # Delete the user (this will trigger our signal)
        self.user1.delete()
        
        # Verify all related data was deleted
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 0)
        self.assertEqual(Message.objects.filter(receiver=self.user1).count(), 0)
        self.assertEqual(Notification.objects.filter(user=self.user1).count(), 0)
        self.assertEqual(MessageHistory.objects.filter(edited_by=self.user1).count(), 0)
        
        # Verify other user's data is still intact
        self.assertEqual(Message.objects.filter(sender=self.user2).count(), 1)
        self.assertEqual(Message.objects.filter(receiver=self.user2).count(), 0)  # The message from user1 was deleted
        self.assertEqual(Notification.objects.filter(user=self.user2).count(), 0)  # Notification about deleted message should be gone
    
    def test_delete_account_view_requires_authentication(self):
        ""Test that delete account view requires authentication."""
        url = reverse('messaging:delete_account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login
    
    def test_delete_account_view_accessible_to_authenticated_users(self):
        ""Test that authenticated users can access the delete account page."""
        self.client.force_login(self.user1)
        url = reverse('messaging:delete_account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    def test_delete_account_api_endpoint(self):
        ""Test the API endpoint for account deletion."""
        self.client.force_login(self.user1)
        url = reverse('messaging:api_delete_account')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Verify user was deleted
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
    
    def test_cannot_delete_other_users_account(self):
        ""Test that users can only delete their own account."""
        # User1 logs in
        self.client.force_login(self.user1)
        
        # Try to delete user2's account
        url = reverse('messaging:api_delete_account')
        response = self.client.post(url)
        
        # Should be successful (deletes own account)
        self.assertEqual(response.status_code, 200)
        
        # Verify user1 was deleted, not user2
        self.assertFalse(User.objects.filter(id=self.user1.id).exists())
        self.assertTrue(User.objects.filter(id=self.user2.id).exists())
