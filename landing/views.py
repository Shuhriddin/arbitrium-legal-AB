from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
import json
import urllib.request
import urllib.parse
import threading
from .models import Application, BlogPost, CourtCase

# View to render main index page with dynamic database objects
def index(request):
    posts = BlogPost.objects.filter(is_published=True)[:6] # Recent 6 articles
    cases = CourtCase.objects.all()[:6] # Recent 6 successful cases
    
    context = {
        'posts': posts,
        'cases': cases,
    }
    return render(request, 'landing/index.html', context)


# Silent GET redirect to change language session key
def set_language(request):
    lang = request.GET.get('lang', 'uz')
    if lang in ['uz', 'ru']:
        request.session['django_language'] = lang
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('index')


# Telegram notification function to send lead information
def send_telegram_notification(app):
    token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
    chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
    
    # Do not execute if credentials are not configured
    if not token or not chat_id:
        return
        
    category_display = dict(app.CATEGORY_CHOICES).get(app.category, app.category)
    message = (
        f"🔔 YANGI MUROJAAT (Lending):\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"👤 F.I.Sh: {app.name}\n"
        f"📞 Tel: {app.phone}\n"
        f"📂 Bo'lim: {category_display}\n"
        f"💬 Muammo: {app.description or 'Tavsif qoldirilmagan.'}"
    )
    
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        data = urllib.parse.urlencode({'chat_id': chat_id, 'text': message}).encode('utf-8')
        req = urllib.request.Request(url, data=data, method='POST')
        
        # Execute network post with a timeout
        with urllib.request.urlopen(req, timeout=5) as response:
            pass
    except Exception as e:
        # Prevent logging errors from crashing the page response
        print(f"Telegram notification failed: {e}")


@require_POST
def submit_application(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            name = data.get('name')
            phone = data.get('phone')
            category = data.get('category')
            description = data.get('description', '')
        else:
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            category = request.POST.get('category')
            description = request.POST.get('description', '')

        # Basic validations
        if not name or not phone or not category:
            return JsonResponse({
                'success': False, 
                'error': 'Barcha maydonlar to\'ldirilishi shart.'
            }, status=400)
            
        valid_categories = ['criminal', 'administrative', 'civil', 'business']
        if category not in valid_categories:
            return JsonResponse({
                'success': False, 
                'error': 'Noto\'g\'ri yo\'nalish tanlandi.'
            }, status=400)

        # Create application and save to database
        application = Application.objects.create(
            name=name,
            phone=phone,
            category=category,
            description=description
        )
        
        # Dispatch Telegram notification in background thread to avoid network blocking
        thread = threading.Thread(target=send_telegram_notification, args=(application,))
        thread.start()
        
        return JsonResponse({
            'success': True,
            'id': application.id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
