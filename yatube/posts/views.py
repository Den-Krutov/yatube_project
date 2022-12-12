from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    template = 'posts/index.html'
    return HttpResponse(render(request, template))


def group_posts(request, slug_str):
    template = 'posts/group_list.html'
    return HttpResponse(render(request, template))
