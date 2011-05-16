import copy
import random
from datetime import datetime,date,timedelta
from decimal import Decimal

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import SetPasswordForm

from emo.userprofile import forms as upforms
from emo.userprofile import models as pmodels
from emo.journal import models as jmodels

def demo(request):
	
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('summary'))

	created = False
	while not created:
		password = "blue%sbird" % random.randint(1,99999)
		guest, created = User.objects.get_or_create(username="guest_%s" % random.randint(1,999))
		guest.set_password(password)
		guest.save()
	
	guest = authenticate(username=guest.username,password=password)
	login(request,guest)
	guest.profile_set.update(is_guest=True)
	
	return HttpResponseRedirect(reverse('summary'))

def demo_activate(request):
	userform = upforms.ActivateForm(request.POST or None)
	pwform = SetPasswordForm(request.user,request.POST or None)
	if request.POST and userform.is_valid() and pwform.is_valid():

		user = request.user
		user.username = userform.cleaned_data.get('username')
		user.email = userform.cleaned_data.get('email')
		user.save()

		profile = user.profile_set.latest('created')
		profile.is_guest = False
		profile.save()		

		pwform.save()
	
		messages.success(request, 'Your account has officially been activated, we hope you enjoy using Emovolution!')	
		return HttpResponseRedirect(reverse('summary'))

	return render_to_response('userprofile/demo_activate_form.html', {'forms': [userform, pwform]}, context_instance=RequestContext(request))

def edit_profile(request,form_class=upforms.UserProfileForm):

	try:
		userprofile = pmodels.Profile.objects.get(user=request.user)
	except pmodels.Profile.DoesNotExist:
		userprofile = None

	form = form_class(request.POST or None,instance=userprofile)
	if request.POST and form.is_valid():
		
		new_profile = form.save(commit=False)
		new_profile.user = request.user
		new_profile.created = datetime.now()
		new_profile.save()

		messages.success(request, 'Profile saved')	
		return HttpResponseRedirect(reverse('profile_edit'))

	return render_to_response('userprofile/profile.html', {'form': form}, context_instance=RequestContext(request))

def main(request):
	
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('summary'))

	date_range = (date.today() - timedelta(days=20), date.today())

	# we'll get back to this when there are more females on this site	
	"""
	males =	jmodels.MoodTrend.objects.filter(entrydate__range=date_range,entry__user__profile__gender="m"
		).values('value','entrydate','moodname','username').distinct().order_by('entrydate')
	males_mood_per_day = {}
	for m in males:
		key = str(m['entrydate'])
		if key not in males_mood_per_day:
			males_mood_per_day[key] = []

		males_mood_per_day[key].append(Decimal("%.1f" % m['value']))
	males_final = [(k,"%.1f" % (sum(v) / (len(v) or 1))) for k,v in males_mood_per_day.iteritems()]

	females = jmodels.MoodTrend.objects.filter(entrydate__range=date_range,entry__user__profile__gender="f"
		).values('value','entrydate','moodname','username').distinct().order_by('entrydate')
	females_mood_per_day = {}
	for m in females:
		key = str(m['entrydate'])
		if key not in females_mood_per_day:
			females_mood_per_day[key] = []

		females_mood_per_day[key].append(Decimal("%.1f" % m['value']))
	females_final = [(k,"%.1f" % (sum(v) / (len(v) or 1))) for k,v in females_mood_per_day.iteritems()]
	"""

	users =	jmodels.MoodTrend.objects.filter(entrydate__range=date_range,
		).values('value','entrydate','moodname','username').distinct().order_by('entrydate')
	users_mood_per_day = {}
	for u in users:
		key = str(u['entrydate'])
		if key not in users_mood_per_day:
			users_mood_per_day[key] = []

		users_mood_per_day[key].append(Decimal("%.1f" % u['value']))
	users_final = [(k,"%.1f" % (sum(v) / (len(v) or 1))) for k,v in users_mood_per_day.iteritems()]

	return render_to_response('main.html', {'form': upforms.LoginForm(), \
			'stats': {'users_mood': users_final}}, context_instance=RequestContext(request))
