import requests

from celery import shared_task
from datetime import date

from django.conf import settings

from todo.models import Task


@shared_task
def send_task_notification():

    tasks = Task.objects.filter(completed=False)

    for task in tasks:
        if task.due_date == date.today():
            message = f"🔔 Напоминание о задаче!\n\n"
            message += f"📌 *{task.title}*\n"
            if task.description:
                message += f"📄 {task.description}\n"
            message += f"📅 Срок выполнения: *{task.due_date}*\n"
            if task.category:
                message += f"📁 Категория: {task.category.name}\n"

            send_telegram_message.delay(
                chat_id=task.user.telegram_id,
                message=message
            )


@shared_task
def send_telegram_message(chat_id, message):

    url = f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage"

    payload = {
        'chat_id': chat_id,
        'text': message,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print(f"Ошибка отправки сообщения: {e}")
        return False
