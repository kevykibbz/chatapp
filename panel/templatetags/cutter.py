from django import template
import os
register=template.Library()


@register.filter(name='cutter')
def cutter(data):
    if data is not None:
       	return (data[:400]) if len(data) > 400 else data
