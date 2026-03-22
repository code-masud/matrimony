import redis
from django import template
from django.conf import settings

register = template.Library()

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)


@register.filter(name='is_presence')
def is_presence(user):
    if not user or not user.id:
        return False

    return redis_client.sismember('online_users_set', user.id)
