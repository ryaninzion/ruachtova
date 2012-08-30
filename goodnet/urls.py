from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	(r'^post/(?P<id>\d+)/$','post'),
	(r'^post/create/$', 'post_form'),
	(r'^register/$', 'registration'),
	(r'^login/$', 'loginrequest'),
	(r'^logout/$', 'logoutrequest'),
)
