from django.contrib import admin
from .models import ChatModel
# Register your models here.


# admin.site.register(ChatModel)

@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'message', 'thread_name', 'time_stamp']
    search_fields = ['id']
    