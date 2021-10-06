import markdown
from django import template
from django.utils.safestring import mark_safe
from decimal import *

register = template.Library()

@register.filter()
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

@register.filter()
def pyung(value):
    return value / 3.3

@register.filter()
def pyungd(value):
    return value / Decimal('3.3')

@register.filter()
def pricepyungd(value, arg):
    return value // (arg / Decimal('3.3'))

@register.filter()
def priceratio(value, arg):
    if value == 0:
        return 0
    return round((arg / 10000) / value * 100)

@register.filter()
def manwon(value):
    return value // 10000

@register.filter()
def intcommak(value):
    value_str = str(value)
    result = ''
    while 0 < len(value_str):
        if result:
            result = ',' + result
        result = value_str[-4:] + result
        value_str = value_str[:-4]
    return result
