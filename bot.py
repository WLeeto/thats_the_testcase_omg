import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_notifier.settings")
# Сетап джанги надо проводить до вызова бота иначе падает бот
django.setup()

import telebot  # noqa: E402
from django.db import IntegrityError  # noqa: E402

from notifier.models import Subscriber  # noqa: E402

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


def subscribe(message: telebot.types.Message) -> None:
    """
    Обрабатывает команду /start: подписывает пользователя на уведомления.
    Если уже подписан — обновляет никнейм.
    :param message: объект сообщения Telegram
    """
    chat_id = message.from_user.id
    nickname = message.from_user.username or ""
    try:
        Subscriber.objects.create(chat_id=chat_id, nickname=nickname)
        bot.send_message(chat_id, "Вы подписались на уведомления о входе в админку.")
    except IntegrityError:
        Subscriber.objects.filter(chat_id=chat_id).update(nickname=nickname)
        bot.send_message(chat_id, "Вы уже подписаны. Никнейм обновлён.")


def unsubscribe(message: telebot.types.Message) -> None:
    """
    Обрабатывает команду /stop: отписывает пользователя от уведомлений.
    :param message: объект сообщения Telegram
    """
    chat_id = message.from_user.id
    deleted, _ = Subscriber.objects.filter(chat_id=chat_id).delete()
    if deleted:
        bot.send_message(chat_id, "Вы отписались от уведомлений.")
    else:
        bot.send_message(chat_id, "Вы не были подписаны.")


bot.message_handler(commands=["start"])(subscribe)
bot.message_handler(commands=["stop"])(unsubscribe)

if __name__ == "__main__":
    print("Бот запущен")
    bot.polling()
