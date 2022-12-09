from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse('Main page')


def group_list(request):
    return HttpResponse('Group list')


def group_posts(request, slug_str):
    return HttpResponse(f'Posts group {slug_str}')
