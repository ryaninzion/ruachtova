from django import template
register = template.Library()

@register.filter('widget_type')
def widget_type(ob):
	return ob.__class__.__name__