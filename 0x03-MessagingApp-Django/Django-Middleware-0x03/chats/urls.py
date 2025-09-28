from django.urls import path, include
from rest_framework_nested import routers
from .views import ConversationViewSet, MessageViewSet

# Use NestedDefaultRouter instead of DefaultRouter
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# If you want messages nested under conversations
conversations_router = routers.NestedDefaultRouter(router, r"conversations", lookup="conversation")
conversations_router.register(r"messages", MessageViewSet, basename="conversation-messages")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversations_router.urls)),
]
