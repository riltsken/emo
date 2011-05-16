from django.contrib import admin
from emo.journal import models as jmodels

class EntryAdmin(admin.ModelAdmin):
	list_display = ('user','date','created',)

admin.site.register(jmodels.Entry, EntryAdmin)

