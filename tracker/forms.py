from django import forms
from django.contrib.auth.models import User
from emo.tracker import models as tmodels
from emo.tracker import choices

class GroupForm(forms.ModelForm):
	
	def __init__(self,user,*args,**kwargs):
		self._user = user
		super(GroupForm,self).__init__(*args,**kwargs)

	def save(self,*args,**kwargs):
		group = super(GroupForm, self).save(commit=False,*args,**kwargs)

		try:
			group.user
		except User.DoesNotExist:
			group.user = self._user

		group.save()
		return group

	class Meta:
		model = tmodels.TrackGroup
		exclude = ('active',)

class TrackerForm(forms.ModelForm):
	data_type = forms.ChoiceField(choices=choices.DATA_TYPES)

	def __init__(self,group,*args,**kwargs):
		self._group = group
		super(TrackerForm,self).__init__(*args,**kwargs)
		self.fields.keyOrder = [
            'label',
			'data_type',
			'field',
		]


	def save(self,*args,**kwargs):
		tracker = super(TrackerForm, self).save(commit=False,*args,**kwargs)

		try:
			tracker.group
		except tmodels.Tracker.DoesNotExist:
			tracker.group = self._group

		tracker.save()
		return tracker

	class Meta:
		model = tmodels.Tracker
		exclude = ('group','active',)
