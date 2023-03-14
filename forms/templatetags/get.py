from django import template

register = template.Library()

@register.filter
def get(value, key):
    if type(value) == dict:
        return value.get(key)
