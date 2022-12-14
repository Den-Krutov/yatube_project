from django.shortcuts import render, get_object_or_404
from .models import Post, Group


# Create your views here.
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'title': 'Последние обновления на сайте',
        'text': 'Это главная страница проекта Yatube',
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug_str):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug_str)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
