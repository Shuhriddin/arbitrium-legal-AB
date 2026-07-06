from django.db import models
import uuid

class ChatSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name="Sessiya ID")
    client_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mijoz ismi")
    client_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Mijoz telefoni")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Boshlangan vaqt")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="So'nggi faollik")
    is_active = models.BooleanField(default=True, verbose_name="Faol")

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Yozishmalar (Chat)"
        ordering = ['-updated_at']

    def __str__(self):
        name = self.client_name or f"Mehmon #{str(self.session_id)[:8]}"
        phone_suffix = f" ({self.client_phone})" if self.client_phone else ""
        return f"{name}{phone_suffix}"

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'Mijoz'),
        ('admin', 'Admin'),
    )
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages', verbose_name="Sessiya")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES, verbose_name="Yuboruvchi")
    message = models.TextField(verbose_name="Xabar")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqt")
    is_read = models.BooleanField(default=False, verbose_name="O'qildimi")

    class Meta:
        verbose_name = "Chat xabari"
        verbose_name_plural = "Chat xabarlari"
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.upper()}: {self.message[:30]}"
