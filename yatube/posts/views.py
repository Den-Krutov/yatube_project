from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    template = 'posts/index.html'
    context = {
        'title': 'Последние обновления на сайте',
        'text': 'Это главная страница проекта Yatube',
    }
    return HttpResponse(render(request, template, context))


def group_posts(request, slug_str):
    template = 'posts/group_list.html'
    context = {
        'title': 'Лев Толстой – зеркало русской революции',
        'text': 'Здесь будет информация о группах проекта Yatube',
    }
    return HttpResponse(render(request, template, context))
