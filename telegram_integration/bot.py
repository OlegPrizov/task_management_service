import telebot
from django.conf import settings

from .services import link_telegram_account

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    parts = message.text.split(maxsplit=1)

    if len(parts) != 2:
        bot.send_message(
            message.chat.id,
            'Отправь команду в формате:\n/start <код>\n\nКод возьми на сайте.'
        )
        return

    code = parts[1].strip()

    success, text = link_telegram_account(
        code=code,
        chat_id=str(message.chat.id),
        telegram_username=message.from_user.username,
    )

    if success:
        bot.send_message(message.chat.id, f'✅ {text}')
    else:
        bot.send_message(message.chat.id, f'❌ {text}')