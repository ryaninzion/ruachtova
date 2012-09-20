from django.conf.urls.defaults import *

urlpatterns = patterns('goodnet.views',
	url(r'^post/(?P<id>\d+)/$','post'),
	url(r'^event/(?P<id>\d+)/$','event'),
	url(r'^initiative/(?P<id>\d+)/$','initiative'),
	url(r'^post/create/$', 'post_form'),
	url(r'^post/bookmark/(?P<type>\w{0,10})/(?P<id>\d+)/$', 'bookmark'),
	url(r'^post/joincause/(?P<type>\w{0,10})/(?P<id>\d+)/$', 'join_cause'),
	url(r'^profile/(?P<id>\d+)/add-photos/$', 'photo_form'),
	url(r'^profile/(?P<id>\d+)/$', 'profile'),
	url(r'^profile/add-friend/(?P<id>\d+)/$', 'add_friend'),
	url(r'^register/$', 'registration'),
	url(r'^profile-edit/(?P<id>\d+)/$', 'profile_edit'),
	url(r'^search/$', 'search_results'),
	url(r'^login/$', 'loginrequest'),
	url(r'^logout/$', 'logoutrequest'),
)
