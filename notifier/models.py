from django.db import models


class Subscriber(models.Model):
    chat_id = models.BigIntegerField(unique=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["nickname"], name="idx_subscriber_nickname"),
        ]

    def __str__(self):
        return str(self.chat_id)
