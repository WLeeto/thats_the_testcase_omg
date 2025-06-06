from unittest.mock import patch

import pytest

from notifier.models import Subscriber
from notifier.tasks import notify_all_admin_login_task


@pytest.mark.django_db
def test_notify_all_admin_login_task_handles_telegram_error():
    # Создаём тестового подписчика
    Subscriber.objects.create(chat_id=123456789)
    with patch("notifier.tasks.bot") as mock_bot:
        mock_bot.send_message.side_effect = Exception("Telegram API unavailable")
        notify_all_admin_login_task("2025-05-06 15:00:00", "admin")
        assert mock_bot.send_message.called
