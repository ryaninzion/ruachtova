from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	(r'^post/(?P<id>\d+)/$','post'),
	(r'^post/create/$', 'post_form'),
	(r'^profile/(?P<id>\d+)/$', 'profile'),
	(r'^register/$', 'registration'),
	(r'^profile-edit/$', 'profile_edit'),
	(r'^login/$', 'loginrequest'),
	(r'^logout/$', 'logoutrequest'),
)
