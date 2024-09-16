import datetime
from django import template

register = template.Library()
@register.simple_tag

def todays_date():
    return datetime.datetime.now().strftime("%d %b, %Y")