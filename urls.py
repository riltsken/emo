import os
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views

admin.autodiscover()
handler500 = 'emo.views.server_error'

urlpatterns = patterns('django.views.generic.simple',
    url(r'^about/$',					'direct_to_template',	{'template':'about.html'},		name="about"),
    url(r'^terms/$',					'direct_to_template',	{'template':'terms.html'},		name="terms"),
    url(r'^privacy/$',					'direct_to_template',	{'template':'privacy.html'},	name="privacy"),
	url(r'^account/activate/complete/$',auth_views.login,										name="reg_act_complete"),
	url(r'^account/logout/$',			auth_views.logout,		{'template_name': 'registration/logout.html', 'next_page': '/'},name="auth_logout"),
) + patterns('',
    url(r'^m/account/login',		'emo.views.mobile_login', name='mobile_login'),
) + patterns('',
    url(r'^$',					'emo.userprofile.views.main',			name="main"),
    url(r'^demo/$',				'emo.userprofile.views.demo',			name="demo"),
    url(r'^demo/activate/$',	'emo.userprofile.views.demo_activate',	name="demo_activate"),
    (r'^',						include('emo.journal.urls')),
    (r'^',						include('emo.social.urls')),
	(r'^profile/',				include('emo.userprofile.urls')),
	(r'^tracker/',				include('emo.tracker.urls')),
    (r'^account/',				include('registration.backends.default.urls')),
    (r'^feedback/',				include('djangovoice.urls')),
	(r'^comments/',				include('django.contrib.comments.urls')),
    (r'^admin/',				include(admin.site.urls)),
	(r'^announcements/',		include('announcements.urls')),
	url(r'^announcements/archive/', 'emo.views.announcement_archive',	name="announcements_archive"),
	url(r'^account/password/change/$', 'django.contrib.auth.views.password_change', {'post_change_redirect': '/profile/'},\
																		name='auth_password_change'),
)

if settings.USE_CUSTOM_CSS:
	urlpatterns.extend(patterns('',
			(r'^media/(?P<path>.*)$', "django.views.static.serve", {'document_root': '%s/media' % os.getcwd(), 'show_indexes': True})
		)
	)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^500/$', 'emo.views.server_error'),
    )
