from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from notifier.telegram_notify import notify_all_admin_login


@receiver(user_logged_in)
def on_user_logged_in(sender, request, user, **kwargs):
    if request.path.startswith('/admin'):
        login_time = timezone.localtime()
        notify_all_admin_login(login_time.strftime('%Y-%m-%d %H:%M:%S'), user.username)
