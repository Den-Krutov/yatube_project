from django.views.generic.base import TemplateView


class AboutAuthorPageView(TemplateView):
    template_name = 'about/author.html'


class AboutTechPageView(TemplateView):
    template_name = 'about/tech.html'
