import secrets
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    telegram_chat_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True
    )
    telegram_username = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    vk_user_id = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True
    )

    def __str__(self):
        return self.username

class TelegramLinkCode(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='telegram_link_codes'
    )
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_for_user(cls, user):
        return cls.objects.create(
            user=user,
            code=secrets.token_urlsafe(24),
            expires_at=timezone.now() + timedelta(minutes=15)
        )

    def __str__(self):
        return f'{self.user.username}: {self.code}'

class VkLinkCode(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vk_link_codes'
    )
    code = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.expires_at

    @classmethod
    def create_for_user(cls, user):
        return cls.objects.create(
            user=user,
            code=secrets.token_urlsafe(24),
            expires_at=timezone.now() + timedelta(minutes=15)
        )

    def __str__(self):
        return f'{self.user.username}: {self.code}'