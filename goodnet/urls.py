from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	(r'^event/(?P<id>\d+)/$','event'),
	(r'^post/(?P<id>\d+)/$','post')
)
