from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
import json
import urllib.request
import urllib.parse
import threading
from .models import ChatSession, ChatMessage

def send_telegram_alert(session, text_message=None):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    if not token or not chat_id:
        return
        
    client_name = session.client_name or f"Mehmon #{str(session.session_id)[:8]}"
    client_phone = session.client_phone or "Kiritilmagan"
    
    # Construct change url for the admin
    # Note: we use a fallback if request is not available
    admin_path = f"/admin/chat/chatsession/{session.id}/change/"
    
    if text_message:
        message = (
            f"💬 CHAT: YANGI XABAR\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Kimdan: {client_name}\n"
            f"📞 Tel: {client_phone}\n"
            f"📝 Xabar: {text_message}\n\n"
            f"👉 Javob berish: {admin_path}\n"
            f"🆔 #CS_{session.id}"
        )
    else:
        message = (
            f"🚀 YANGI CHAT BOSHLANDI\n"
            f"━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Mijoz: {client_name}\n"
            f"📞 Tel: {client_phone}\n\n"
            f"👉 Chatni ko'rish: {admin_path}\n"
            f"🆔 #CS_{session.id}"
        )
        
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message}).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        with urllib.request.urlopen(req, timeout=5) as response:
            pass
    except Exception as e:
        print(f"Telegram notification failed: {e}")

@csrf_exempt
@require_POST
def init_chat(request):
    try:
        data = json.loads(request.body) if request.body else {}
        session_id_str = data.get('session_id')
        
        session = None
        created = False
        
        if session_id_str:
            try:
                session = ChatSession.objects.filter(session_id=session_id_str).first()
            except Exception:
                pass
                
        if not session:
            session = ChatSession.objects.create()
            created = True
            
            # Send Telegram alert about new chat session
            thread = threading.Thread(target=send_telegram_alert, args=(session,))
            thread.start()
            
        return JsonResponse({
            'success': True,
            'session_id': str(session.session_id),
            'client_name': session.client_name or '',
            'client_phone': session.client_phone or '',
            'is_created': created
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_GET
def get_messages(request):
    session_id_str = request.GET.get('session_id')
    if not session_id_str:
        return JsonResponse({'success': False, 'error': 'Session ID is required'}, status=400)
        
    session = ChatSession.objects.filter(session_id=session_id_str).first()
    if not session:
        return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
        
    # Only mark admin replies as read if the client explicitly requests it (when chat window is open)
    mark_read = request.GET.get('mark_read', 'false').lower() == 'true'
    if mark_read:
        session.messages.filter(sender='admin', is_read=False).update(is_read=True)
    
    messages = session.messages.all().order_by('created_at')
    messages_data = []
    for msg in messages:
        messages_data.append({
            'id': msg.id,
            'sender': msg.sender,
            'message': msg.message,
            'created_at': msg.created_at.strftime('%H:%M'),
            'is_read': msg.is_read
        })
        
    return JsonResponse({
        'success': True,
        'messages': messages_data,
        'client_name': session.client_name or '',
        'client_phone': session.client_phone or ''
    })

@csrf_exempt
@require_POST
def send_message(request):
    try:
        data = json.loads(request.body)
        session_id_str = data.get('session_id')
        text = data.get('message', '').strip()
        
        if not session_id_str or not text:
            return JsonResponse({'success': False, 'error': 'session_id and message are required'}, status=400)
            
        session = ChatSession.objects.filter(session_id=session_id_str).first()
        if not session:
            return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
            
        message = ChatMessage.objects.create(
            session=session,
            sender='user',
            message=text
        )
        
        # Update session timestamp
        session.save()
        
        # Alert lawyer via Telegram
        thread = threading.Thread(target=send_telegram_alert, args=(session, text))
        thread.start()
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'sender': message.sender,
                'message': message.message,
                'created_at': message.created_at.strftime('%H:%M'),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def update_profile(request):
    try:
        data = json.loads(request.body)
        session_id_str = data.get('session_id')
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        if not session_id_str or (not name and not phone):
            return JsonResponse({'success': False, 'error': 'session_id and either name or phone are required'}, status=400)
            
        session = ChatSession.objects.filter(session_id=session_id_str).first()
        if not session:
            return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
            
        if name:
            session.client_name = name
        if phone:
            session.client_phone = phone
            
        session.save()
        
        # Alert lawyer about profile update
        not_changed = "O'zgarmadi"
        name_str = name or not_changed
        phone_str = phone or not_changed
        alert_text = f"Foydalanuvchi aloqa ma'lumotlarini qoldirdi:\nIsm: {name_str}\nTel: {phone_str}"
        thread = threading.Thread(target=send_telegram_alert, args=(session, alert_text))
        thread.start()
        
        return JsonResponse({
            'success': True,
            'client_name': session.client_name,
            'client_phone': session.client_phone
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
@require_POST
def reply_from_telegram(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return JsonResponse({'success': False, 'error': 'Missing or invalid authorization header'}, status=401)
        
    token = auth_header.split(' ')[1]
    if token != settings.TELEGRAM_BOT_TOKEN:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=401)
        
    try:
        data = json.loads(request.body)
        session_id_db = data.get('session_id')
        text = data.get('message', '').strip()
        
        if not session_id_db or not text:
            return JsonResponse({'success': False, 'error': 'session_id and message are required'}, status=400)
            
        session = ChatSession.objects.filter(id=session_id_db).first()
        if not session:
            return JsonResponse({'success': False, 'error': 'Session not found'}, status=404)
            
        message = ChatMessage.objects.create(
            session=session,
            sender='admin',
            message=text
        )
        
        session.save()
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': message.id,
                'sender': message.sender,
                'message': message.message,
                'created_at': message.created_at.strftime('%H:%M'),
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
