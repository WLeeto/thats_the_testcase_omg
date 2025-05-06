import csv

from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone

from .models import Subscriber


@admin.action(description="Экспортировать выбранных подписчиков в CSV")
def export_subscribers_csv(modeladmin, request, queryset):
    """Экспорт выбранных подписчиков в CSV-файл."""
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="subscribers_{timezone.now().date()}.csv"'
    writer = csv.writer(response)
    writer.writerow(["chat_id", "nickname", "subscribed_at"])
    for sub in queryset:
        writer.writerow([sub.chat_id, sub.nickname, sub.subscribed_at])
    return response


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """Административный интерфейс для управления подписчиками."""

    list_display = ("chat_id", "nickname", "subscribed_at")
    search_fields = ("chat_id", "nickname")
    ordering = ("-subscribed_at",)
    actions = [export_subscribers_csv]
    list_filter = ("subscribed_at",)
