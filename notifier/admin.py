from django.contrib import admin
from .models import Subscriber


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'nickname', 'subscribed_at')
    search_fields = ('chat_id', 'nickname')
    ordering = ('-subscribed_at',)
