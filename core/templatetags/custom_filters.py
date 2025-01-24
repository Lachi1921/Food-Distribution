from django import template
from datetime import datetime

register = template.Library()

@register.filter
def calc_price(value, arg):
    try:
        final_price = value / 3 * arg
        return int(final_price)
    except (TypeError, ValueError):
        return value

@register.simple_tag
def current_year():
    return datetime.now().year