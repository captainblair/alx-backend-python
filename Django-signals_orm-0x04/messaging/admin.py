from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Message, Notification, MessageHistory


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('edited_at', 'edited_by', 'content_preview')
    can_delete = False
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'is_read', 'was_edited', 'view_history')
    list_filter = ('is_read', 'edited', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp', 'edited', 'view_history')
    inlines = [MessageHistoryInline]
    
    def was_edited(self, obj):
        return obj.edited
    was_edited.boolean = True
    was_edited.short_description = 'Edited'
    
    def view_history(self, obj):
        if obj.edit_history.exists():
            url = reverse('admin:messaging_messagehistory_changelist') + f'?message__id__exact={obj.id}'
            return format_html('<a href="{}">View Edit History</a>', url)
        return "No edits"
    view_history.short_description = 'Edit History'


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'message_link', 'edited_by', 'edited_at', 'content_preview')
    list_filter = ('edited_at', 'edited_by')
    search_fields = ('message__content', 'edited_by__username')
    date_hierarchy = 'edited_at'
    readonly_fields = ('message', 'edited_by', 'edited_at', 'content')
    
    def message_link(self, obj):
        url = reverse('admin:messaging_message_change', args=[obj.message.id])
        return format_html('<a href="{}">{}</a>', url, f'Message {obj.message.id}')
    message_link.short_description = 'Message'
    
    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__content')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
