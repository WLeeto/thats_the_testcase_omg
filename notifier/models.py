from datetime import datetime

from django.db import models


class Subscriber(models.Model):
    """
    Модель подписчика Telegram-бота.
    :param chat_id: уникальный идентификатор чата Telegram
    :param nickname: никнейм пользователя
    :param subscribed_at: дата и время подписки
    """

    chat_id: int = models.BigIntegerField(unique=True)
    nickname: str = models.CharField(max_length=50, blank=True, null=True)
    subscribed_at: "datetime" = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["nickname"], name="idx_subscriber_nickname"),
        ]

    def __str__(self) -> str:
        """Строковое представление подписчика."""
        return str(self.chat_id)
