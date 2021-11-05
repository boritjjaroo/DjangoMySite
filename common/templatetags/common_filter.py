import markdown
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter()
def boolean_yn(value):
    if value:
        return '예'
    return '아니오'

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)

@register.filter
def list_item(l, i):
    try:
        return l[i]
    except:
        return None
