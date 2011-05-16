from datetime import datetime
import operator

from django import forms
from django.db.models import Q
from django.contrib.auth.models import User

from emo.journal import models as jmodels
from emo.moods.models import Mood
from emo.utils.fields import SliderField

class SearchForm(forms.Form):

	search_type = forms.ChoiceField(choices=[('all', 'All'),('journal',
		'Journal'),('tags','Tags')],widget=forms.widgets.RadioSelect,required=False)
	query = forms.CharField(max_length=200)

	def get_results(self,results):

		text = self.cleaned_data.get('query', None)

		# wrap the tags in a q object and then operator OR them to get the
		# filter
		if self.cleaned_data.get('search_type') == 'tags':
			tags = [Q(tags__contains=t.strip()) for t in text.split(',')]
			tags = reduce(operator.__or__, tags)
			return results.filter(tags)

		if self.cleaned_data.get('search_type') == 'journal':
			return results.filter(journal__contains=text)

		return results.filter(Q(journal__contains=text)|Q(tags__contains=text))

	# makes it easy to go through the string query as if it were tags, and bold
	# them in the html. Might need another method for this, like doing
	# highlighting via JS or something.
	def query_list(self):

		if hasattr(self, 'cleaned_data') and self.cleaned_data.get('query', None):
			return [q.strip() for q in self.cleaned_data.get('query', '').split(',')]
		return []

class DateForm(forms.Form):

	start = forms.DateField(required=False)
	end = forms.DateField(required=False)

class MoodForm(forms.Form):

	def __init__(self,moods,*args,**kwargs):

		super(MoodForm,self).__init__(*args,**kwargs)

		min_value = 0
		max_value = 9
		slide_width = 15
		slide_height = 28
		bg_width = 343
		bg_height = 30
		slide_img = "img/new/slidericon.jpg"
		bg_img = "img/new/sliderbase.jpg"
		step = 1

		self.field_names = {}
		for m in moods:

			value = m.get('value',5)
			name = ''.join(m.get('name').split(' ')) # There is an issue with the slider and spacing in the text, but it works as a label

			self.field_names.update({m.get('name'): name}) # used for the save method to find the striped out name

			self.fields[name] = SliderField(
				min_value=min_value,max_value=max_value,slide_width=slide_width,slide_height=slide_height,\
				bg_width=bg_width,bg_height=bg_height,slide_img=slide_img,bg_img=bg_img,step=step)

			self.fields[name].label = m.get('name')
			self.fields[name].initial = value

	# remove the old moodtrend objects then update with the new ones
	# NOTE: This is not a modelform, there is no super() for this save method
	def save(self,entry,username):

		jmodels.MoodTrend.objects.filter(entry=entry).delete()

		# Confusing myself a bit... do we really need to query for name__in? Seems like we have some weird edge case here, sigh.
		moods = Mood.objects.filter(user__username=username, name__in=self.field_names.keys())
		for m in moods:
			v = self.cleaned_data.get(self.field_names[m.name])
			jmodels.MoodTrend.objects.create(entry=entry,mood=m,value=v,username=username,entrydate=entry.date,moodname=m.name)

	def clean(self,*args,**kwargs):
		cleaned_data = super(MoodForm,self).clean(*args,**kwargs)

		# prevent people from messing with POST variables, they shouldn't be able to get values exceeding 10 or below 1
		for v in cleaned_data.values():
			if v > 10:
				raise forms.ValidationError("The value cannot exceed 10.")
			if v < 1:
				raise forms.ValidationError("The value cannot dip below 1.")

		return cleaned_data

class EntryForm(forms.ModelForm):

	def __init__(self,given_date,request_user,*args,**kwargs):

		super(EntryForm,self).__init__(*args,**kwargs)

		self.request_user = request_user

		self.fields['tags'].widget.attrs['style'] = "height: 100px; margin-bottom: 20px;"
		self.given_date = given_date

	def save(self,*args,**kwargs):

		entry = super(EntryForm, self).save(commit=False,*args,**kwargs)

		try:
			entry.user
		except User.DoesNotExist:
			entry.user = self.request_user

		if not entry.created:
			entry.created = datetime.now()

		if not entry.date:
			entry.date = self.given_date

		# get rid of extraneous whitespace from the tags
		tags = []
		for t in entry.tags.split(','):
			tags.append(t.strip())
		tags = ','.join(tags)

		# set entry.tags to null by default, if we had tags then use those.
		entry.tags = None
		if tags:
			entry.tags = tags

		if kwargs.get('commit',True) == True:
		    entry.save()

		return entry

	class Meta:

		model = jmodels.Entry
