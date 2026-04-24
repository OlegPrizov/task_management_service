from django.conf import settings
from django.utils import timezone
import requests

from users.models import TelegramLinkCode, User


def link_telegram_account(code: str, chat_id: str, telegram_username: str | None = None):
    try:
        link = TelegramLinkCode.objects.select_related('user').get(
            code=code,
            is_used=False,
        )
    except TelegramLinkCode.DoesNotExist:
        return False, 'Код не найден или уже использован'

    if link.expires_at < timezone.now():
        return False, 'Код истек, получи новый на сайте'

    user = link.user
    user.telegram_chat_id = str(chat_id)
    user.telegram_username = telegram_username or ''
    user.save(update_fields=['telegram_chat_id', 'telegram_username'])

    link.is_used = True
    link.save(update_fields=['is_used'])

    return True, f'Telegram успешно подключен к аккаунту {user.username}'


def send_telegram_message(chat_id: str, text: str) -> bool:
    if not settings.TELEGRAM_BOT_TOKEN:
        return False

    url = f'https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage'
    response = requests.post(
        url,
        json={
            'chat_id': chat_id,
            'text': text,
        },
        timeout=10,
    )
    return response.ok