from django.contrib import admin
from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
