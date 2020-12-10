
from django import template
register = template.Library()

@register.filter
def footer_message(data):
    return 'Denvolcimento web com Django 2.0.2'

@register.filter
def arredonda(value, casas):
    return round(value, casas)