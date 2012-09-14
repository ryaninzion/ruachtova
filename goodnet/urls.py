from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	url(r'^post/(?P<id>\d+)/$','post'),
	url(r'^post/create/$', 'post_form'),
	url(r'^post/bookmark/(?P<id>\d+)/$', 'bookmark'),
	url(r'^post/joincause/(?P<id>\d+)/$', 'join_cause'),
	url(r'^profile/(?P<id>\d+)/add-photos/$', 'photo_form'),
	url(r'^profile/(?P<id>\d+)/$', 'profile'),
	url(r'^profile/add-friend/(?P<id>\d+)/$', 'add_friend'),
	url(r'^register/$', 'registration'),
	url(r'^profile-edit/(?P<id>\d+)/$', 'profile_edit'),
	url(r'^login/$', 'loginrequest'),
	url(r'^logout/$', 'logoutrequest'),
)
