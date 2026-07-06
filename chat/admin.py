from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from django.utils.html import format_html
from django.utils.timezone import localtime
import json
from .models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('sender', 'message', 'created_at', 'is_read')
    can_delete = False
    ordering = ('created_at',)

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('client_display', 'client_phone', 'message_count', 'unread_count_display', 'created_at', 'updated_at', 'is_active')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('client_name', 'client_phone', 'session_id')
    readonly_fields = ('session_id', 'created_at', 'updated_at')
    
    # Custom change form template
    change_form_template = 'admin/chat/chatsession/change_form.html'
    
    # Inlines will allow seeing messages as fallback even if JS doesn't run
    inlines = [ChatMessageInline]

    def client_display(self, obj):
        return obj.client_name or f"Mehmon #{str(obj.session_id)[:8]}"
    client_display.short_description = "Mijoz"
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Xabarlar"
    
    def unread_count_display(self, obj):
        count = obj.messages.filter(sender='user', is_read=False).count()
        if count > 0:
            return format_html('<span style="background-color: #d9534f; color: white; padding: 3px 8px; border-radius: 10px; font-weight: bold;">{} ta yangi</span>', count)
        return "0"
    unread_count_display.short_description = "O'qilmagan"

    # Register custom admin endpoints inside ModelAdmin
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<path:object_id>/reply-ajax/', self.admin_site.admin_view(self.reply_ajax), name='chat_chatsession_reply_ajax'),
            path('<path:object_id>/messages-ajax/', self.admin_site.admin_view(self.messages_ajax), name='chat_chatsession_messages_ajax'),
        ]
        return custom_urls + urls
        
    def reply_ajax(self, request, object_id):
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Invalid method'}, status=400)
        
        try:
            session = self.get_object(request, object_id)
            if not session:
                return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
                
            data = json.loads(request.body)
            text = data.get('message', '').strip()
            
            if not text:
                return JsonResponse({'success': False, 'error': 'Message text is required'}, status=400)
                
            message = ChatMessage.objects.create(
                session=session,
                sender='admin',
                message=text
            )
            # Update session's updated_at timestamp
            session.save() 
            
            return JsonResponse({
                'success': True,
                'message': {
                    'id': message.id,
                    'sender': message.sender,
                    'message': message.message,
                    'created_at': localtime(message.created_at).strftime('%H:%M'),
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def messages_ajax(self, request, object_id):
        session = self.get_object(request, object_id)
        if not session:
            return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
            
        # Mark all user messages in this session as read when admin loads the chat AJAX-wise
        session.messages.filter(sender='user', is_read=False).update(is_read=True)
        
        messages = session.messages.all().order_by('created_at')
        msg_list = []
        for m in messages:
            msg_list.append({
                'id': m.id,
                'sender': m.sender,
                'message': m.message,
                'created_at': localtime(m.created_at).strftime('%d.%m.%Y %H:%M'),
                'is_read': m.is_read
            })
            
        return JsonResponse({
            'success': True,
            'client_name': session.client_name or f"Mehmon #{str(session.session_id)[:8]}",
            'client_phone': session.client_phone or "Kiritilmagan",
            'messages': msg_list
        })
