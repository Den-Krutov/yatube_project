from django.core.paginator import Paginator

LIMIT = 10


def get_page_obj(request, objects):
    """Converts objects in instance Page with request"""
    paginator = Paginator(objects, LIMIT)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
