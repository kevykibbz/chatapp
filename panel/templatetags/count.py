from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from panel.models import ChatModel
register=template.Library()


@register.filter(name='count')
def count(data):
    if data is not None:
    	count=ChatModel.objects.filter(receiver=data,is_read=False).count()
    	if count > 0:
    		return intcomma(count)
