from general.models import Message, Subscriber
from django.contrib import admin

# Register your models here.
admin.site.register(Subscriber)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message', 'seen', 'reply', 'created_at']
