from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'messaging'

urlpatterns = [
    # Thread views
    path(
        'threads/',
        login_required(views.ThreadListView.as_view()),
        name='thread_list',
    ),
    
    # Unread messages API
    path(
        'api/messages/unread/',
        views.unread_messages_api,
        name='api_unread_messages',
    ),
    
    # Mark messages as read API
    path(
        'api/messages/mark-read/',
        views.mark_as_read_api,
        name='api_mark_read',
    ),
    path(
        'threads/<int:pk>/',
        login_required(views.ThreadDetailView.as_view()),
        name='thread_detail',
    ),
    
    # User account management
    path(
        'account/delete/',
        login_required(views.DeleteUserView.as_view()),
        name='delete_account',
    ),
    
    # API endpoints
    path(
        'api/threads/',
        login_required(views.thread_list_api),
        name='api_thread_list',
    ),
    path(
        'api/threads/<int:other_user_id>/',
        login_required(views.thread_list_api),
        name='api_user_threads',
    ),
    path(
        'api/threads/<int:other_user_id>/<int:message_id>/',
        login_required(views.thread_list_api),
        name='api_thread_detail',
    ),
    path(
        'api/account/delete/',
        login_required(views.delete_user_api),
        name='api_delete_account',
    ),
]
