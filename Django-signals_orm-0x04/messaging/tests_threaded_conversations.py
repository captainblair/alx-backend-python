from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import connection

from .models import Message
from .thread_utils import get_threaded_messages, get_conversation_threads

User = get_user_model()

class ThreadedConversationTests(TestCase):
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
        
        # Create a conversation thread
        self.root_message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Hello, user2!'
        )
        
        self.reply1 = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='Hi user1, how are you?',
            parent_message=self.root_message
        )
        
        self.reply2 = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="I'm good, thanks!",
            parent_message=self.reply1
        )
        
        # Create another conversation
        self.other_message = Message.objects.create(
            sender=self.user2,
            receiver=self.user1,
            content='This is a different conversation'
        )
    
    def test_thread_creation(self):
        ""Test that replies are properly linked."""
        self.assertEqual(self.root_message.replies.count(), 1)
        self.assertEqual(self.reply1.replies.count(), 1)
        self.assertEqual(self.reply2.replies.count(), 0)
        
        self.assertEqual(self.reply1.parent_message, self.root_message)
        self.assertEqual(self.reply2.parent_message, self.reply1)
    
    def test_thread_updated_timestamp(self):
        ""Test that thread_updated is properly set on replies."""
        # Refresh from database
        root = Message.objects.get(pk=self.root_message.pk)
        self.assertGreaterEqual(root.thread_updated, self.root_message.thread_updated)
    
    def test_get_threaded_messages(self):
        ""Test the get_threaded_messages utility function."""
        threads = get_threaded_messages(self.user1.id)
        
        # Should return both conversations
        self.assertEqual(len(threads), 2)
        
        # Find our test thread
        thread = next(t for t in threads if t['id'] == self.root_message.id)
        
        # Check thread structure
        self.assertEqual(len(thread['replies']), 1)  # First level reply
        self.assertEqual(thread['replies'][0]['id'], self.reply1.id)
        self.assertEqual(len(thread['replies'][0]['replies']), 1)  # Second level reply
        self.assertEqual(thread['replies'][0]['replies'][0]['id'], self.reply2.id)
    
    def test_get_conversation_threads_specific(self):
        ""Test getting a specific thread by message ID."""
        result = get_conversation_threads(
            user_id=self.user1.id,
            other_user_id=self.user2.id,
            message_id=self.root_message.id
        )
        
        self.assertEqual(result['id'], self.root_message.id)
        self.assertEqual(len(result['replies']), 1)
        self.assertEqual(result['replies'][0]['id'], self.reply1.id)
    
    def test_get_conversation_threads_all(self):
        ""Test getting all threads between two users."""
        result = get_conversation_threads(
            user_id=self.user1.id,
            other_user_id=self.user2.id
        )
        
        # Should return both threads (one in each direction)
        self.assertEqual(len(result['threads']), 2)
    
    def test_query_optimization(self):
        ""Test that we're using select_related and prefetch_related properly."""
        with self.assertNumQueries(3):  # 1 for messages, 1 for replies, 1 for users
            threads = get_threaded_messages(self.user1.id)
            
            # Access related data to ensure queries are executed
            for thread in threads:
                _ = thread['sender']
                for reply in thread.get('replies', []):
                    _ = reply['sender']
    
    def test_thread_depth_limitation(self):
        ""Test that we don't have infinite recursion."""
        # Create a deep thread
        current = self.root_message
        for i in range(15):  # More than our default max_depth of 10
            current = Message.objects.create(
                sender=self.user1 if i % 2 else self.user2,
                receiver=self.user2 if i % 2 else self.user1,
                content=f'Message {i}',
                parent_message=current
            )
        
        # Should not raise RecursionError
        threads = get_threaded_messages(self.user1.id)
        
        # Check that the depth was limited
        def check_depth(thread, depth=0, max_depth=10):
            if depth > max_depth:
                self.fail('Thread depth exceeds maximum')
            for reply in thread.get('replies', []):
                check_depth(reply, depth + 1, max_depth)
        
        for thread in threads:
            check_depth(thread)
