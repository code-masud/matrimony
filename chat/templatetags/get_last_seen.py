import redis
from django import template
from django.conf import settings
from datetime import datetime

register = template.Library()

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


@register.filter('get_last_seen')
def get_last_seen(user):
    if not user or not user.id:
        return None

    ts = redis_client.get(f"last_seen:{user.id}")
    if ts is None:
        return None 
    try:
        ts = float(ts.decode("utf-8"))
    except AttributeError:
        ts = float(ts)  # in case Redis returned string already

    return datetime.fromtimestamp(ts)