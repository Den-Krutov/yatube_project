from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})


@register.filter
def uglify(field):
    uglify_field = ''
    for char in field:
        if len(uglify_field) % 2:
            uglify_field += char.upper()
        else:
            uglify_field += char.lower()
    return uglify_field
