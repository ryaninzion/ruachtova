from django import template
register = template.Library()

@register.filter('widget_type')
def widget_type(ob):
	return ob.__class__.__name__

@register.filter('verbose_name') 
def verbose_name(object):
	return object._meta.verbose_name