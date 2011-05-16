from django.conf.urls.defaults import *

urlpatterns = patterns('emo.tracker.views',
	url('^add-group/$',										'group_form',		name="tracker_group_add"),
	url('^(?P<group_id>\d+)/edit/$',						'group_form',		name="tracker_group_edit"),
	url('^(?P<group_id>\d+)/$',								'group',			name="tracker_group"),
	url('^(?P<group_id>\d+)/add-tracker$',					'tracker_form',		name="tracker_tracker_add"),
	url('^(?P<group_id>\d+)/(?P<track_id>\d+)/edit$',		'tracker_form',		name="tracker_tracker_edit"),
	url('^(?P<group_id>\d+)/(?P<track_id>\d+)/',			'tracker_fillout',	name="tracker_tracker_fillout"),
)
