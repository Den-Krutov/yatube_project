"""Manage app posts."""
from django.contrib import admin

from .models import Comment, Follow, Group, Post


class CommentInline(admin.StackedInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    """Convenient representation of posts for management."""
    inlines = [
        CommentInline,
    ]
    list_display = (
        'pk',
        'text',
        'created',
        'author',
        'group',
    )
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


class FollowAdmin(admin.ModelAdmin):
    """Convenient representation of follows for management."""

    list_display = (
        'pk',
        'user',
        'author',
    )
    list_editable = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('author',)
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'post',
        'author',
        'text',
    )
    search_fields = ('text',)
    list_filter = ('post',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)
admin.site.register(Group)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
