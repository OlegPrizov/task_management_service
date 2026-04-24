import vk_api
from django.conf import settings
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from .services import link_vk_account, send_vk_message


vk_session = vk_api.VkApi(token=settings.VK_GROUP_TOKEN)
longpoll = VkBotLongPoll(vk_session, settings.VK_GROUP_ID)


def run_vk_bot():
    for event in longpoll.listen():
        if event.type != VkBotEventType.MESSAGE_NEW:
            continue

        message = event.object.message
        text = message.get('text', '').strip()
        user_id = message.get('from_id')

        if not text or not user_id:
            continue

        success, response = link_vk_account(
            code=text,
            vk_user_id=str(user_id),
        )

        prefix = '✅' if success else '❌'
        send_vk_message(str(user_id), f'{prefix} {response}')