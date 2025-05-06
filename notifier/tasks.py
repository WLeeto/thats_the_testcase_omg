from celery_app import shared_task
from notifier.models import Subscriber
import telebot
import os
import logging

logger = logging.getLogger(__name__)
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '123456:FAKE_FOR_TESTS')
bot = telebot.TeleBot(TOKEN)

@shared_task
def notify_all_admin_login_task(login_time, username):
    message = f'Дата входа: {login_time}\nИмя пользователя: {username}'
    for sub in Subscriber.objects.all():
        try:
            bot.send_message(sub.chat_id, message)
        except Exception as e:
            logger.error(f"Ошибка отправки сообщения chat_id={sub.chat_id}: {e}")
