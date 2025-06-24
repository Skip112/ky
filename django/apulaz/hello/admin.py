from django.contrib import admin
from .models import Topic, Post  # Импортируй нужные модели

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at')  # Поля, которые будут отображаться в списке
    search_fields = ('title', 'author__username')  # Поля, по которым можно искать

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('topic', 'author', 'created_at', 'content')
    search_fields = ('content', 'author__username')
