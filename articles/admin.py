from django.contrib import admin
from .models import Article, Comment
# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title',
        'body',
        'author',
    ]

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)