from django.contrib import admin
from .models import User, Chat, ChatMessage, Memory, Reminder

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(Memory)
admin.site.register(Reminder)
