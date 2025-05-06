import os
import telebot
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_notifier.settings')
django.setup()

from notifier.models import Subscriber
from django.db import IntegrityError

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def subscribe(message):
    chat_id = message.chat.id
    nickname = message.from_user.username or ''
    try:
        Subscriber.objects.create(chat_id=chat_id, nickname=nickname)
        bot.send_message(chat_id, 'Вы подписались на уведомления о входе в админку.')
    except IntegrityError:
        # Обновляем никнейм, если пользователь уже есть
        Subscriber.objects.filter(chat_id=chat_id).update(nickname=nickname)
        bot.send_message(chat_id, 'Вы уже подписаны. Никнейм обновлён.')

@bot.message_handler(commands=['stop'])
def unsubscribe(message):
    chat_id = message.chat.id
    deleted, _ = Subscriber.objects.filter(chat_id=chat_id).delete()
    if deleted:
        bot.send_message(chat_id, 'Вы отписались от уведомлений.')
    else:
        bot.send_message(chat_id, 'Вы не были подписаны.')

if __name__ == '__main__':
    print('Бот запущен')
    bot.infinity_polling()
