"""Provides response to requests app posts."""
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Group, Post

COUNT_POSTS_PAGE: int = 10


def index(request):
    """Display all posts."""
    template = 'posts/index.html'
    posts = Post.objects.select_related('author', 'group')
    paginator = Paginator(posts, COUNT_POSTS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """Display all posts group."""
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    paginator = Paginator(posts, COUNT_POSTS_PAGE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)
