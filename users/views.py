from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import TelegramLinkCode, VkLinkCode


@login_required
def notification_settings(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'telegram_disconnect':
            request.user.telegram_chat_id = None
            request.user.telegram_username = None
            request.user.save(update_fields=['telegram_chat_id', 'telegram_username'])

            TelegramLinkCode.objects.filter(user=request.user, is_used=False).delete()
            messages.success(request, 'Telegram отвязан')
            return redirect('users:notification_settings')

        if action == 'telegram_reconnect':
            request.user.telegram_chat_id = None
            request.user.telegram_username = None
            request.user.save(update_fields=['telegram_chat_id', 'telegram_username'])

            TelegramLinkCode.objects.filter(user=request.user, is_used=False).delete()
            messages.success(request, 'Создан новый код для привязки Telegram')
            return redirect('users:notification_settings')
        
        if action == 'vk_disconnect':
            request.user.vk_user_id = None
            request.user.save(update_fields=['vk_user_id'])

            VkLinkCode.objects.filter(
                user=request.user,
                is_used=False
            ).delete()

            messages.success(request, 'VK отвязан')
            return redirect('users:notification_settings')


        if action == 'vk_reconnect':
            request.user.vk_user_id = None
            request.user.save(update_fields=['vk_user_id'])

            VkLinkCode.objects.filter(
                user=request.user,
                is_used=False
            ).delete()

            messages.success(request, 'Создан новый код для привязки VK')
            return redirect('users:notification_settings')

    telegram_link_code = None

    if not request.user.telegram_chat_id:
        TelegramLinkCode.objects.filter(
            user=request.user,
            is_used=False,
            expires_at__lt=timezone.now()
        ).delete()

        telegram_link_code = TelegramLinkCode.objects.filter(
            user=request.user,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()

        if telegram_link_code is None:
            telegram_link_code = TelegramLinkCode.create_for_user(request.user)
    
    vk_link_code = None

    if not request.user.vk_user_id:
        VkLinkCode.objects.filter(
            user=request.user,
            is_used=False,
            expires_at__lt=timezone.now()
        ).delete()

        vk_link_code = VkLinkCode.objects.filter(
            user=request.user,
            is_used=False,
            expires_at__gt=timezone.now()
        ).order_by('-created_at').first()

        if vk_link_code is None:
            vk_link_code = VkLinkCode.create_for_user(request.user)

    return render(request, 'users/notification_settings.html', {
        'telegram_link_code': telegram_link_code,
        'vk_link_code': vk_link_code,
    })