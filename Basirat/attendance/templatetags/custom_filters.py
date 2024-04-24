# custom_filters.py
from django import template

from main.models import Group

register = template.Library()


@register.simple_tag
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='convert_seconds_to_minutes')
def convert_seconds_to_minutes(seconds):
    """
    Convert seconds to minutes and remaining seconds.
    """
    if seconds is None:
        return None
    seconds = seconds - 3
    minutes = seconds // 60
    remaining_seconds = seconds % 60

    return {'minutes': minutes, 'seconds': remaining_seconds}


@register.simple_tag(name='get_all_groups')
def get_all_groups():
    return Group.objects.all()
