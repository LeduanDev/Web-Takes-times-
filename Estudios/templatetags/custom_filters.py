
from django import template
from datetime import timedelta

register = template.Library()


@register.filter(name="duration_format")
def duration_format(value):
    if isinstance(value, timedelta):
        seconds = value.total_seconds()
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
    return value


@register.filter(name="duration_format2")
def duration_format2(value, format_type='hh:mm:ss'):
    if isinstance(value, timedelta):
        seconds = value.total_seconds()

        if format_type == 'ss':
            return int(seconds)
        elif format_type == 'mm':
            # Limitar a 2 decimales
            return "{:.2f}".format(seconds / 60)
        else:
            hours, remainder = divmod(seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            return "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))

    return value
