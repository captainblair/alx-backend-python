from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, ListView, DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, Http404
from django.db.models import Q, Prefetch, Count

from .models import Message, MessageHistory
User = get_user_model()

@method_decorator(login_required, name='dispatch')
class DeleteUserView(SuccessMessageMixin, DeleteView):
    """
    View for users to delete their own account.
    """
    model = User
    template_name = 'messaging/delete_user_confirm.html'
    success_url = reverse_lazy('login')
    success_message = "Your account has been successfully deleted."
    
    def get_object(self, queryset=None):
        """Return the user to be deleted."""
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        """Override delete to add success message."""
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response


@method_decorator(login_required, name='dispatch')
class ThreadListView(ListView):
    """View to display all message threads for the current user."""
    model = Message
    template_name = 'messaging/thread_list.html'
    context_object_name = 'threads'
    paginate_by = 20
    
    def get_queryset(self):
        """Optimize queries with select_related and prefetch_related."""
        # Get all threads where user is either sender or receiver
        threads = Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user),
            parent_message__isnull=True  # Only root messages
        ).select_related('sender', 'receiver')
        
        # Prefetch replies with optimization
        return threads.prefetch_related(
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'receiver')
                                     .order_by('timestamp'),
                to_attr='prefetched_replies'
            )
        ).order_by('-thread_updated')


@method_decorator(login_required, name='dispatch')
class ThreadDetailView(DetailView):
    """View to display a single thread with all its replies."""
    model = Message
    template_name = 'messaging/thread_detail.html'
    context_object_name = 'message'
    
    def get_queryset(self):
        """Optimize queries for thread detail view."""
        return Message.objects.select_related('sender', 'receiver')
    
    def get_context_data(self, **kwargs):
        """Add thread context with optimized queries."""
        context = super().get_context_data(**kwargs)
        message = self.get_object()
        
        # Get the root message if this is a reply
        root_message = message.get_root()
        
        # Get all messages in the thread with optimized queries
        thread_messages = Message.objects.filter(
            Q(pk=root_message.pk) | Q(parent_message__in=root_message.get_descendants())
        ).select_related('sender', 'receiver').order_by('timestamp')
        
        context['thread_messages'] = thread_messages
        context['root_message'] = root_message
        return context
    
    def get_object(self, queryset=None):
        """Ensure user has permission to view this thread."""
        message = super().get_object(queryset)
        if message.sender != self.request.user and message.receiver != self.request.user:
            raise Http404("You don't have permission to view this thread.")
        return message


def get_threads_for_user(user):
    """Helper function to get threads for a user with optimized queries."""
    # Get all threads where user is either sender or receiver
    threads = Message.objects.filter(
        Q(sender=user) | Q(receiver=user),
        parent_message__isnull=True  # Only root messages
    ).select_related('sender', 'receiver')
    
    # Prefetch replies with optimization
    return threads.prefetch_related(
        Prefetch(
            'replies',
            queryset=Message.objects.select_related('sender', 'receiver')
                                 .order_by('timestamp'),
            to_attr='prefetched_replies'
        )
    ).order_by('-thread_updated')


@login_required
def thread_list_api(request, other_user_id=None, message_id=None):
    """
    API endpoint to get message threads.
    Can return all threads, threads with a specific user, or a specific thread.
    """
    # Optimize queries with select_related and prefetch_related
    threads = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    )
    
    # Filter for specific message thread if message_id is provided
    if message_id:
        thread = get_object_or_404(threads, id=message_id, parent_message__isnull=True)
        thread_messages = Message.objects.filter(
            Q(pk=thread.pk) | Q(parent_message__in=thread.get_descendants())
        ).select_related('sender', 'receiver').order_by('timestamp')
        
        return JsonResponse({
            'thread': {
                'id': thread.id,
                'messages': [{
                    'id': msg.id,
                    'content': msg.content,
                    'timestamp': msg.timestamp,
                    'is_read': msg.is_read,
                    'sender': {
                        'id': msg.sender.id,
                        'username': msg.sender.username,
                        'email': msg.sender.email,
                    },
                    'receiver': {
                        'id': msg.receiver.id,
                        'username': msg.receiver.username,
                        'email': msg.receiver.email,
                    }
                } for msg in thread_messages]
            }
        })
    
    # Filter for specific user if other_user_id is provided
    if other_user_id:
        other_user = get_object_or_404(User, id=other_user_id)
        threads = threads.filter(
            (Q(sender=request.user) & Q(receiver=other_user)) |
            (Q(sender=other_user) & Q(receiver=request.user))
        )
    
    # Get root messages (thread starters) with optimization
    root_messages = threads.filter(parent_message__isnull=True)
    
    # Prefetch related data to reduce queries
    root_messages = root_messages.select_related('sender', 'receiver').prefetch_related(
        Prefetch(
            'replies',
            queryset=Message.objects.select_related('sender', 'receiver')
                                 .filter(Q(sender=request.user) | Q(receiver=request.user))
                                 .order_by('timestamp'),
            to_attr='prefetched_replies'
        )
    ).order_by('-thread_updated')
    
    # Prepare response data
    thread_data = []
    for thread in root_messages:
        other_user = thread.sender if thread.receiver == request.user else thread.receiver
        
        # Get unread count for this thread
        unread_count = sum(
            1 for reply in getattr(thread, 'prefetched_replies', []) 
            if not reply.is_read and reply.receiver == request.user
        )
        
        thread_data.append({
            'id': thread.id,
            'content': thread.content,
            'timestamp': thread.timestamp,
            'thread_updated': thread.thread_updated,
            'other_user': {
                'id': other_user.id,
                'username': other_user.username,
                'email': other_user.email,
            },
            'unread_count': unread_count,
            'reply_count': len(getattr(thread, 'prefetched_replies', [])),
            'latest_reply': thread.prefetched_replies[-1].timestamp if hasattr(thread, 'prefetched_replies') and thread.prefetched_replies else None
        })
    
    return JsonResponse({'threads': thread_data})


@require_http_methods(["POST"])
@login_required
def delete_user_api(request):
    """
    API endpoint for programmatic user deletion.
    Returns JSON response instead of HTML.
    """
    try:
        user = request.user
        user.delete()
        return JsonResponse({"status": "success", "message": "User deleted successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
