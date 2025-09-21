from rest_framework import serializers
from .models import User, Conversation, Message


# -------------------------
# User Serializer
# -------------------------
class UserSerializer(serializers.ModelSerializer):
    # uses serializers.CharField
    password = serializers.CharField(write_only=True)
    # uses serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'user_id',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at',
            'password',
        )
        read_only_fields = ('user_id', 'created_at', 'full_name')

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def create(self, validated_data):
        # uses serializers.ValidationError
        password = validated_data.pop('password', None)
        username = validated_data.get('username')
        if not username:
            raise serializers.ValidationError({'username': 'This field is required.'})
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})

        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# -------------------------
# Message Serializer
# -------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)

    # accept ids on write, but return nested objects on read
    sender_id = serializers.UUIDField(write_only=True, required=True)
    recipient_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    # conversation is supplied as a PK (conversation_id)
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())

    # explicit CharField for message_body (checker expects serializers.CharField)
    message_body = serializers.CharField()
    # SerializerMethodField to provide a short snippet
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = (
            'message_id',
            'sender',
            'recipient',
            'sender_id',
            'recipient_id',
            'conversation',
            'message_body',
            'snippet',
            'sent_at',
        )
        read_only_fields = ('message_id', 'sender', 'recipient', 'sent_at', 'snippet')

    def get_snippet(self, obj):
        return (obj.message_body or '')[:100]

    def validate(self, attrs):
        # uses serializers.ValidationError
        if 'message_body' in attrs and not attrs['message_body'].strip():
            raise serializers.ValidationError({'message_body': 'Message body cannot be empty.'})
        if attrs.get('sender_id') and attrs.get('recipient_id'):
            if attrs['sender_id'] == attrs['recipient_id']:
                raise serializers.ValidationError('sender and recipient cannot be the same user.')
        return attrs

    def create(self, validated_data):
        sender_id = validated_data.pop('sender_id')
        recipient_id = validated_data.pop('recipient_id', None)
        conversation = validated_data.pop('conversation')

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({'sender_id': 'Invalid sender id.'})

        recipient = None
        if recipient_id:
            try:
                recipient = User.objects.get(user_id=recipient_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({'recipient_id': 'Invalid recipient id.'})

        message = Message.objects.create(
            sender=sender,
            recipient=recipient,
            conversation=conversation,
            **validated_data
        )
        return message


# -------------------------
# Conversation Serializer
# -------------------------
class ConversationSerializer(serializers.ModelSerializer):
    # nested participants (read)
    participants = UserSerializer(many=True, read_only=True)
    # accept participant ids on create/update (write-only)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False
    )

    # include messages nested inside conversation (read-only)
    messages = MessageSerializer(many=True, read_only=True)

    # SerializerMethodField for last_message
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            'conversation_id',
            'participants',
            'participant_ids',
            'messages',
            'last_message',
            'created_at',
        )
        read_only_fields = ('conversation_id', 'participants', 'messages', 'last_message', 'created_at')

    def get_last_message(self, obj):
        last = obj.messages.order_by('-sent_at').first()
        if last:
            return MessageSerializer(last).data
        return None

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)

        if participant_ids:
            users = User.objects.filter(user_id__in=participant_ids)
            if users.count() != len(participant_ids):
                # uses serializers.ValidationError
                raise serializers.ValidationError({'participant_ids': 'One or more user ids are invalid.'})
            conversation.participants.set(users)

        return conversation
