from celery import shared_task
from django.utils import timezone

from .models import Task
from telegram_integration.services import send_telegram_message
from vk_integration.services import send_vk_message


@shared_task
def notify_overdue_tasks():
    now = timezone.now()

    overdue_tasks = Task.objects.select_related(
        'creator',
        'executor',
        'project',
    ).filter(
        due_date__lt=now,
        status__in=[Task.Status.TODO, Task.Status.IN_PROGRESS],
        overdue_notified_at__isnull=True,
    )

    for task in overdue_tasks:
        executor_name = task.executor.username if task.executor else 'не назначен'
        project_name = task.project.name if task.project else 'Без проекта'
        due_date = timezone.localtime(task.due_date).strftime('%d.%m.%Y %H:%M')

        text = (
            f'⚠️ Задача просрочена\n\n'
            f'Название: {task.title}\n'
            f'Исполнитель: {executor_name}\n'
            f'Проект: {project_name}\n'
            f'Дедлайн: {due_date}\n'
            f'Статус: {task.get_status_display()}'
        )

        sent_any = False

        telegram_chat_ids = set()

        if task.creator and task.creator.telegram_chat_id:
            telegram_chat_ids.add(task.creator.telegram_chat_id)

        if task.executor and task.executor.telegram_chat_id:
            telegram_chat_ids.add(task.executor.telegram_chat_id)

        for chat_id in telegram_chat_ids:
            if send_telegram_message(chat_id, text):
                sent_any = True

        vk_user_ids = set()

        if task.creator and task.creator.vk_user_id:
            vk_user_ids.add(task.creator.vk_user_id)

        if task.executor and task.executor.vk_user_id:
            vk_user_ids.add(task.executor.vk_user_id)

        for vk_user_id in vk_user_ids:
            if send_vk_message(vk_user_id, text):
                sent_any = True

        if sent_any:
            task.overdue_notified_at = now
            task.save(update_fields=['overdue_notified_at'])