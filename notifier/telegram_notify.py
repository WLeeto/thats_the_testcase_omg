import logging

from notifier.tasks import notify_all_admin_login_task

logger = logging.getLogger(__name__)


def notify_all_admin_login(login_time, username):
    notify_all_admin_login_task.delay(login_time, username)
