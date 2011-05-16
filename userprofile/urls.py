from django.conf.urls.defaults import *

from emo.userprofile.views import edit_profile
from emo.userprofile import forms as upforms

urlpatterns = patterns('',
    url(r'^$',	edit_profile,	name='profile_edit'),
	# not ready for this yet
    #url(r'^settings/$',	edit_profile,	{'form_class': upforms.SettingsProfileForm}, name='profile_edit_settings'),
)
