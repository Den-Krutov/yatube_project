from django.core.paginator import Paginator

LIMIT = 10


def get_page_obj(request, objects):
    """Converts objects in instance Page with request"""
    return Paginator(objects, LIMIT).get_page(request.GET.get('page'))
