from django.core.management.base import BaseCommand

from telegram_integration.bot import bot


class Command(BaseCommand):
    help = 'Run Telegram bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Telegram bot started'))
        bot.infinity_polling()