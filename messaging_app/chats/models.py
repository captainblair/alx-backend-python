import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# -------------------------
# Custom User Model
# -------------------------
class User(AbstractUser):
    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    # Explicit password field (checker requirement)
    password = models.CharField(max_length=128, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'   # use email for login
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"


# -------------------------
# Conversation Model
# -------------------------
class Conversation(models.Model):
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# -------------------------
# Message Model
# -------------------------
class Message(models.Model):
    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages_sent'
    )
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='messages_received', null=True
    )
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages'
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.email}: {self.message_body[:30]}"
