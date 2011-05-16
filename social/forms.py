from django import forms
from django.contrib.auth.models import User

class SearchForm(forms.Form):

	def __init__(self,request_user,*args,**kwargs):

		super(SearchForm,self).__init__(*args,**kwargs)
		self.request_user = request_user
	
		self.fields['search'] = forms.CharField()
