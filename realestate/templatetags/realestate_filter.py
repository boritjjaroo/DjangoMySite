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
    return round(arg / value * 100)

@register.filter()
def priceratio2(value, arg):
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

@register.filter()
def boolean_ox(value):
    if value:
        return 'O'
    return 'X'

@register.filter()
def date_yyyymmdd(value):
    val = f'{value.year:04d}-{value.month:02d}-{value.day:02d}'
    return val
