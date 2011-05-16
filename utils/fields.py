from django import forms
from django.forms.util import flatatt 
from django.template import loader, Context, RequestContext
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.conf import settings

class Slider(forms.widgets.Widget):

	def __init__(self,*args,**kwargs):
		super(Slider,self).__init__()	
		self.kwargs_dict = kwargs.copy()

	def render(self, name, value, attrs=None):

		if value is None:
			value = 5 

		final_attrs = self.build_attrs(attrs, name=name)
		final_attrs['value'] = force_unicode(value)

		context_dict = {'input_attrs': flatatt(final_attrs).replace("\"", ""),}
		context_dict.update({'final_attrs':final_attrs, 'MEDIA_URL': settings.MEDIA_URL})
		context_dict.update(self.kwargs_dict)

		return mark_safe(loader.get_template('fields/slider.html').render(Context(context_dict)))

class SliderField(forms.IntegerField):
	def __init__(self, *args, **kwargs):
		super(SliderField, self).__init__()
		self.widget = Slider(*args,**kwargs)

	def clean(self,value):
		return super(SliderField,self).clean(value)

