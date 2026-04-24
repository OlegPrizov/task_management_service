from django.core.management.base import BaseCommand

from vk_integration.bot import run_vk_bot


class Command(BaseCommand):
    help = 'Run VK bot'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('VK bot started'))
        run_vk_bot()