from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('set-language/', views.set_language, name='set_language'),
    path('submit-application/', views.submit_application, name='submit_application'),
]
