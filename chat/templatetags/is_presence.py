from django import template

register = template.Library()

@register.filter(name='is_presence')
def is_presence(user):
    if not user or not user.username:
        return False
    return True