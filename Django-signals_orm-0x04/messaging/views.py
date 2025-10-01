from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.decorators.http import require_http_methods

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
        ""Return the user to be deleted."""
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        ""Override delete to add success message."""
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response


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
