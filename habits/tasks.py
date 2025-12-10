import datetime

import requests
from django.contrib.messages.context_processors import messages

from config import settings
from celery import shared_task

from habits.models import Habit
from habits.services import send_telegram_bot


@shared_task
def send_telegram():
    """Отправка напоминания о том, в какое время какие привычки необходимо выполнять."""
    habit = Habit.objects.all()
    current_date = datetime.datetime.now()
    for h in habit:
        if h.time <= current_date:
            chat_id = h.user.tg_chat_id
            message = f"""
                Вам нужно выполнить: {h.description}
                Место: {h.place}
                Время: {h.time}
            """
            send_telegram_bot(message, chat_id)





