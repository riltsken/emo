from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered

from emo.userprofile import models as umodels

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user','created',)	
admin.site.register(umodels.Profile, ProfileAdmin)
class HistoryProfileAdmin(admin.ModelAdmin):
	list_display = ('user','created',)	
admin.site.register(umodels.HistoryProfile, HistoryProfileAdmin)

class UserAdmin(admin.ModelAdmin):
	list_display = ('username','email','last_login','date_joined','is_staff')
	list_filter = ('last_login','date_joined')
	search_fields = ('username','email')
	ordering = ('-date_joined',)
	

try:
	admin.site.unregister(User)
except NotRegistered:
	pass 

admin.site.register(User, UserAdmin)
