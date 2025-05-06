import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_notifier.settings')

from django.test import TestCase
from notifier.models import Subscriber
from unittest.mock import patch
from django.utils import timezone
from notifier.tasks import notify_all_admin_login_task

# Create your tests here.

class SubscriberModelTest(TestCase):
    def test_subscribe_and_unsubscribe(self):
        chat_id = 123456
        sub = Subscriber.objects.create(chat_id=chat_id)
        self.assertEqual(Subscriber.objects.count(), 1)
        self.assertEqual(sub.chat_id, chat_id)
        sub.delete()
        self.assertEqual(Subscriber.objects.count(), 0)

class NotifyAllAdminLoginTest(TestCase):
    @patch('notifier.tasks.bot.send_message')
    def test_notify_all_admin_login(self, mock_send):
        Subscriber.objects.create(chat_id=111)
        Subscriber.objects.create(chat_id=222)
        dt = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
        username = 'admin'
        notify_all_admin_login_task(dt, username)
        self.assertEqual(mock_send.call_count, 2)
        for call in mock_send.call_args_list:
            args, kwargs = call
            self.assertIn('Дата входа', args[1])
            self.assertIn('Имя пользователя', args[1])
