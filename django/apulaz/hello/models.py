from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Модель темы форума
class Topic(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Модель сообщения в теме
class Post(models.Model):
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.author.username} on {self.topic.title}'
    
# Модель блокировки отправки сообщений
User.add_to_class('blocked_until', models.DateTimeField(null=True, blank=True))
