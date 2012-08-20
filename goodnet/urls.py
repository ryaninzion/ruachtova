from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	(r'^event/(?P<id>\d+)/$','event')
)
