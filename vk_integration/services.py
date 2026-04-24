import random

import vk_api
from django.conf import settings
from django.utils import timezone

from users.models import VkLinkCode


vk_session = vk_api.VkApi(token=settings.VK_GROUP_TOKEN)
vk = vk_session.get_api()


def link_vk_account(code: str, vk_user_id: str):
    try:
        link = VkLinkCode.objects.select_related('user').get(
            code=code,
            is_used=False,
        )
    except VkLinkCode.DoesNotExist:
        return False, 'Код не найден или уже использован'

    if link.expires_at < timezone.now():
        return False, 'Код истек, получи новый на сайте'

    user = link.user
    user.vk_user_id = str(vk_user_id)
    user.save(update_fields=['vk_user_id'])

    link.is_used = True
    link.save(update_fields=['is_used'])

    return True, f'VK успешно подключен к аккаунту {user.username}'


def send_vk_message(vk_user_id: str, text: str) -> bool:
    try:
        vk.messages.send(
            user_id=int(vk_user_id),
            message=text,
            random_id=random.randint(1, 2_147_483_647),
        )
        return True
    except Exception:
        return False