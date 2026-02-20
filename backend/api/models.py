from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Extended User with profile fields."""
    bio = models.TextField(blank=True, default='')
    location = models.CharField(max_length=255, blank=True, default='')
    title = models.CharField(max_length=255, blank=True, default='')
    photo_url = models.URLField(blank=True, default='')
    settings = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.email or self.username


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    title = models.CharField(max_length=255, default='New Chat')
    last_message = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.title} ({self.user})"


class ChatMessage(models.Model):
    ROLE_CHOICES = [('user', 'User'), ('ai', 'AI')]

    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"


class Memory(models.Model):
    CATEGORY_CHOICES = [
        ('conversations', 'Conversations'),
        ('documents', 'Documents'),
        ('daily-briefings', 'Daily Briefings'),
        ('important', 'Important'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memories')
    title = models.CharField(max_length=255)
    snippet = models.TextField(blank=True, default='')
    type = models.CharField(max_length=100, default='Note')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Memories'

    def __str__(self):
        return self.title


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    text = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)
    due_date = models.CharField(max_length=100, blank=True, default='')
    tag = models.CharField(max_length=100, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text
