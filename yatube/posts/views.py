"""Provides response to requests app posts."""
from django.shortcuts import get_object_or_404, render

from .models import Group, Post

COUNT_POSTS_PAGE: int = 10


def index(request):
    """Display all posts."""
    template = 'posts/index.html'
    posts = Post.objects.select_related('author', 'group')[:COUNT_POSTS_PAGE]
    context = {
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Display all posts group."""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')[:COUNT_POSTS_PAGE]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
