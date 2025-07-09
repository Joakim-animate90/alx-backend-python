from django.urls import path
from .views import get_message_thread

urlpatterns = [
    path('thread/<int:message_id>/', get_message_thread, name='message_thread'),
]
