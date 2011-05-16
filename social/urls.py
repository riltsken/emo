from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from emo.social.views import edit_relationship as er

urlpatterns = patterns('emo.social.views',
	url('^community/search/$',			'search',											name="social_search"),
	url('^community/$',					'view_relatives',									name="social_list"),

	url('^community/bookmark/add/$',	er,			{'field': 'bookmarked',	'value': 1},	name="social_bookmark_add"),
	url('^community/bookmark/remove/$',	er,			{'field': 'bookmarked',	'value': 0},	name="social_bookmark_remove"),
	url('^community/request/add$',		er,			{'field': 'pending',	'value': 1},	name="social_request_add"),
	url('^community/request/remove$',	er,			{'field': 'pending',	'value': 0},	name="social_request_remove"),
	url('^community/request/approve/$',	er,			{'field': 'approved',	'value': 1},	name="social_request_approve"),
	url('^community/request/deny/$',	er,			{'field': 'approved',	'value': 0},	name="social_request_deny"),
	url('^community/blocked/add/$',		er,			{'field': 'blocked',	'value': 1},	name="social_block"),
	url('^community/blocked/remove/$',	er,			{'field': 'blocked',	'value': 0},	name="social_unblock"),
)
