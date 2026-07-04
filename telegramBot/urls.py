from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('botuser', BotUserViewset)
router.register('channels', TelegramChannelViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', GetUser.as_view()),
    path('lang/', ChangeUserLanguage.as_view()),
    path('channel/', GetTelegramChannel.as_view()),
    path('delete_channel/', DeleteTelegramChannel.as_view()),
]