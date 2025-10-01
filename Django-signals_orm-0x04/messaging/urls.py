from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'messaging'

urlpatterns = [
    # User account management
    path(
        'account/delete/',
        login_required(views.DeleteUserView.as_view()),
        name='delete_account',
    ),
    
    # API endpoints
    path(
        'api/account/delete/',
        login_required(views.delete_user_api),
        name='api_delete_account',
    ),
]
