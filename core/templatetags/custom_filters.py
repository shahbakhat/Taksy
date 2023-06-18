from django import template
from datetime import datetime, timedelta
from django.utils import timezone


register = template.Library()

@register.filter
def format_pickup_datetime(pickup_datetime):
    today = timezone.now().date()
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)

    if pickup_datetime.date() == today:
        pickup_date = 'Today'
    elif pickup_datetime.date() == tomorrow:
        pickup_date = 'Tomorrow'
    elif pickup_datetime.date() == yesterday:
        pickup_date = 'Yesterday'
    else:
        pickup_date = pickup_datetime.strftime('%Y-%m-%d')

    return f"{pickup_date} {pickup_datetime.strftime('%H:%M')}"
