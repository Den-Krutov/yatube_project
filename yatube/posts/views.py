"""Provides response to requests app posts."""
from functools import partial

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .helpers import get_page_obj
from .models import Comment, Group, Post, User


def index(request):
    """Display all posts."""
    posts = Post.objects.prefetch_related('author', 'group')
    return render(request,
                  'posts/index.html',
                  context={'page_obj': get_page_obj(request, posts)})


def group_posts(request, slug):
    """Display all posts group."""
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related('author')
    return render(request,
                  'posts/group_list.html',
                  context={'group': group,
                           'page_obj': get_page_obj(request, posts)})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.select_related('group')
    return render(request,
                  'posts/profile.html',
                  context={'author': author,
                           'page_obj': get_page_obj(request, posts)})


def post_detail(request, post_id):
    post = get_object_or_404(Post.objects.select_related('author', 'group'),
                             pk=post_id)
    form = CommentForm()
    comments = Comment.objects.select_related('author').filter(post=post)
    return render(request,
                  'posts/post_detail.html',
                  context={'post': post,
                           'form': form,
                           'comments': comments})


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        return redirect('posts:profile', request.user.username)
    return render(request, 'posts/create_post.html', context={'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.prefetch_related('author', 'group'),
                             pk=post_id)
    get_redirected_page = partial(redirect,
                                  'posts:post_detail',
                                  post_id=post.pk)
    if request.user != post.author:
        return get_redirected_page()
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post,
    )
    if form.is_valid():
        form.save()
        return get_redirected_page()
    return render(request,
                  'posts/create_post.html',
                  context={'form': form, 'is_edit': True})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        form.instance.author = request.user
        form.instance.post = post
        form.save()
    return redirect('posts:post_detail', post_id)
