from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('emo.journal.views',
	# looking at a different user / public urls
	url('^u/(?P<username>\w+)/journal/$',											'journal',			name="journal_specific_user"),
	url('^u/(?P<username>\w+)/journal/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',	'journal_entry',	name="journal_entry_specific_user"),
	url('^u/(?P<username>\w+)/journal/(?P<year>\d+)/(?P<month>\d+)/$',				'journal',			name="journal_month_specific_user"),
	url('^u/(?P<username>\w+)/journal/(?P<year>\d+)/$',								'journal',			name="journal_year_specific_user"),
	url('^u/(?P<username>\w+)/statistics/$',										'stats',			name="stats_specific_user"),
	url('^u/(?P<username>\w+)/search/$',											'entry_search',		name="entry_search_specific_user"),
	url('^u/(?P<username>\w+)/$',													'summary',			name="summary_specific_user"),

	# urls based on request.user
	url('^summary/$',											'summary',			name="summary"),
	url('^search/$',											'entry_search',		name="entry_search"),
	url('^journal/$',											'journal',			name="journal"),
	url('^journal/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',	'journal_entry',	name="journal_entry"),
	url('^journal/(?P<year>\d+)/(?P<month>\d+)/$',				'journal',			name="journal_month"),
	url('^journal/(?P<year>\d+)/$',								'journal',			name="journal_year"),
	url('^statistics/$',										'stats',			name="stats"),
	url('^tags/$',												'manage_tags',		name="tags"),
	url('^share/$',			direct_to_template,	{'template': 'journal/share.html'},	name="share"),

	# some ajaxy urls for use for use from a phone / widget
	url('^w/journal/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'journal_entry_ajax',	name="journal_entry_ajax"),
	url('^w/journal/$', 'journal_entry_ajax',	name="journal_entry_ajax"),

)
