from django.urls import path
from . import views

urlpatterns = [
    path('init/', views.init_chat, name='chat_init'),
    path('messages/', views.get_messages, name='chat_messages'),
    path('send/', views.send_message, name='chat_send'),
    path('update-profile/', views.update_profile, name='chat_update_profile'),
    path('reply-from-telegram/', views.reply_from_telegram, name='chat_reply_from_telegram'),
]
