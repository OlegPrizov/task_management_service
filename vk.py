from vk_integration.services import send_vk_message
from users.models import User

u = User.objects.get(username='oleg')

send_vk_message(u.vk_user_id, 'Тестовое уведомление из Django')