from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	(r'^post/(?P<id>\d+)/$','post'),
	(r'^post/create/$', 'post_form'),
	(r'^register/$', 'registration'),
	(r'^createprofile/$', 'registration2'),
	(r'^login/$', 'loginrequest'),
	(r'^logout/$', 'logoutrequest'),
)
