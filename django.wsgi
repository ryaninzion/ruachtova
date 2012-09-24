import os
import sys
import django.core.handlers.wsgi

path = '/var/django-code/ruachtova/Ruachtova/'
if path not in sys.path:
	sys.path.append(path)
	sys.path.append('/var/django-code/ruachtova/Ruachtova/ruachtova/')
	
os.environ['DJANGO_SETTINGS_MODULE'] = 'ruachtova.settings'

application = django.core.handlers.wsgi.WSGIHandler()
