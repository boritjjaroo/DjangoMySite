import markdown
from django import template
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter()
def boolean_ox(value):
    if value:
        return 'O'
    return 'X'
    
@register.filter()
def boolean_yn(value):
    if value:
        return '예'
    return '아니오'

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))
