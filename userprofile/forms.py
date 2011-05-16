from django import forms
from django.contrib.auth.models import User

from emo.userprofile import models as upmodels
from emo.utils.fields import SliderField

SETTINGS_FIELDS = ['metric_system','timezone','date_display']

class UserProfileForm(forms.ModelForm):
	
	extroversion = forms.CharField(max_length=1)
	def __init__(self,*args,**kwargs):

		super(UserProfileForm,self).__init__(*args,**kwargs)

		min_value = 0
		max_value = 9
		slide_width = 15
		slide_height = 28
		bg_width = 343
		bg_height = 30
		slide_img = "img/new/slidericon.jpg"
		bg_img = "img/new/sliderbase.jpg"
		step = 1
		
		self.fields['extroversion'] = SliderField(
			min_value=min_value,max_value=max_value,slide_width=slide_width,slide_height=slide_height,\
			bg_width=bg_width,bg_height=bg_height,slide_img=slide_img,bg_img=bg_img,step=step)

	class Meta:
		model = upmodels.Profile
		exclude = SETTINGS_FIELDS

class SettingsProfileForm(forms.ModelForm):
	
	class Meta:
		model = upmodels.Profile
		fields = SETTINGS_FIELDS

class LoginForm(forms.Form):

	username = forms.CharField(max_length=100)
	password = forms.CharField(max_length=100,widget=forms.widgets.PasswordInput)

class ActivateForm(forms.Form):
	
	username = forms.CharField(max_length=100)
	email = forms.EmailField()

	def clean_username(self,*args,**kwargs):

		username = self.cleaned_data.get('username')
		if User.objects.filter(username=username).count():
			raise forms.ValidationError('That username is in use. Please try another one.')

		return username


