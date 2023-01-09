from django.core.paginator import Paginator


def get_page_obj(request, objects, limit_objects_page):
    """Converts objects in instance Page with request"""
    paginator = Paginator(objects, limit_objects_page)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
