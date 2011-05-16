import calendar,math
from datetime import datetime, timedelta, date

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Avg
from decimal import Decimal

from emo.journal import forms as jforms
from emo.journal import models as jmodels
from emo.journal import helpers as jhelpers
from emo.userprofile import models as upmodels

class check_permissions:

	def __init__(self, orig_view):

	    self.orig_view = orig_view

	def __call__(self, request, *args, **kwargs):

		username = kwargs.get('username', None)
		if not username or username == request.user.username:
			return self.orig_view(request,*args,**kwargs)

		entrydate = date(int(kwargs.get('year')),int(kwargs.get('month')),int(kwargs.get('day')))

		try:
			entry = jmodels.Entry.objects.get(user__username=username, date=entrydate)
			if entry.is_private:
				messages.info(request, "The entry you are trying to read is set to private.")
				return HttpResponseRedirect(reverse('journal_month_specific_user',kwargs={'username': username, 'year': entrydate.year, 'month': entrydate.month}))
		except jmodels.Entry.DoesNotExist:
			messages.info(request, "An entry does not exist on the specified date.")
			return HttpResponseRedirect(reverse('journal_month_specific_user',kwargs={'username': username, 'year': entrydate.year, 'month': entrydate.month}))

		return self.orig_view(request,*args,**kwargs)

"""
This view allows the editing/viewing of an entry. An entry can only be edited within 4 days of todays date
"""
@check_permissions
def journal_entry(request,username=None,year=None,month=None,day=None):

	now = datetime.now()
	given_date = None
	if year and month and day:
		given_date = date(int(year),int(month),int(day))

	# current entry is the last entry added + 24 hours
	current_entry_date = None
	grace_days = [now.date() - timedelta(days=delta) for delta in range(4)]

	if username:
		mood_values = get_object_or_404(User, username=username).mood_set.values('name')
	else:
		mood_values = request.user.mood_set.values('name')

	try:
		current_entry = jmodels.Entry.objects.get(user__username=username or request.user.username,date__year=year,date__month=month,date__day=day)
		current_entry_date = current_entry.date + timedelta(days=1)
		mood_values = [{'name': mt.moodname, 'value': mt.value} for mt in current_entry.moodtrend_set.all()]
		mood_avg = sum([m['value'] for m in mood_values]) / Decimal(len(mood_values))
		mood_avg = "%.2f" % mood_avg
	except jmodels.Entry.DoesNotExist:
		current_entry = None
		mood_avg = 5

	editable = True
	if not current_entry and given_date and given_date not in grace_days:
		m = "Can't create an entry in the future"
		if now.date() > given_date:
			m = "Can't create an entry that is older than 3 days from today"

		editable = False
		messages.info(request,m)
		return HttpResponseRedirect(reverse('journal'))

	if current_entry_date and current_entry_date < (now.date() - timedelta(days=2)):
		editable = False

	if username and request.user.username != username:
		editable = False

	form = jforms.EntryForm(given_date or now,request.user,request.POST or None,instance=current_entry)
	mood_form = jforms.MoodForm(mood_values,request.POST or None)
	tagcloud = jhelpers.TagCloud(jmodels.Entry.objects.filter(user__username=username or request.user.username),username or request.user.username)

	if request.POST and form.is_valid() and mood_form.is_valid():
		entry = form.save()
		mood_form.save(entry,request.user.username)
		messages.success(request,"Journal entry saved.")
		return HttpResponseRedirect(reverse("journal"))

	return render_to_response('journal/entry.html', {'form': form,'mood_form': mood_form, \
		'mood_values': mood_values, 'mood_avg': mood_avg, 'editable':editable, 'tagcloud':tagcloud, 'entry_date': given_date}, \
		context_instance=RequestContext(request))

def journal_entry_ajax(request,year=None,month=None,day=None):

	entry_date = date.today()
	if year:
		entry_date = date(int(year),int(month),int(day))

	try:
		journal = jmodels.Entry.objects.get(user=request.user,\
			date__year=entry_date.year,date__month=entry_date.month,date__day=entry_date.day)
		mood_values = [{'name': mt.moodname, 'value': mt.value} for mt in current_entry.moodtrend_set.all()]
	except jmodels.Entry.DoesNotExist:
		journal = None
		mood_values = request.user.mood_set.values('name')

	mood_form = jforms.MoodForm(mood_values,request.POST or None)

	return render_to_response('journal/widget_form.html', {'mood_form': mood_form}, context_instance=RequestContext(request))

"""
The summary page has to accomplish:
	1. Show the last 5-10 entries
	2. Show their tagcloud
	3. Have our observer throw them some blurbs
"""
def summary(request,username=None):

	if username:
		profile = upmodels.Profile.objects.filter(user__username=username\
			).select_related('user').latest('created')
		if profile.public:
			username = profile.user.username
		else: # if not a public profile, then take them back home
			messages.warning(request,"Profile does not exist or is set to private")
			return HttpResponseRedirect(reverse('main'))
	else:
		username = request.user.username

	now = date.today()

	# we are going to use these recent entries for two things, summary and
	# trending
	recent_entries = jmodels.Entry.objects.filter(user__username=username)

	summary_entries = recent_entries.exclude(journal='')[:5]
	trend_entries = [x.pk for x in recent_entries[:10]]

	trend = jmodels.MoodTrend.objects.filter(username=username,\
		entry__in=trend_entries)

	r_plot = None
	if trend.count():
		moods = {}
		for m in trend:
			if m.moodname not in moods:
				moods[m.moodname] = []
			moods[m.moodname].append((Decimal(m.value),m.entry.date))

		# get our mood avgs, this will build a radar graph in the html
		mood_avg_values = {}
		for moodname, values in moods.iteritems():
			value_total = 0
			for v in values:
				value_total += v[0]

			mood_avg_values[moodname] = "%.2f" % (value_total / len(values))

		# radar plot
		k_v = mood_avg_values.items()
		k_v.sort()
		rp = []
		rp.append("cht=r") # chart type. r = radar
		rp.append("chs=325x325") # chart size. height x width
		rp.append("chxt=x,y") # char axis, x and y
		rp.append("chxs=0,676767,10,0,l,676767") # chart axis label sizes
		rp.append("chxr=1,1,10") # chart range
		rp.append("chds=1,10") # not sure
		rp.append("chd=t:%s,%s" % ( ",".join([avg[1] for avg in k_v]), k_v[0][1] ))
		rp.append("chco=FF0000") # color of plot
		rp.append("chls=2") # who knows
		rp.append("chm=B,FF000080,0,1.0,5.0") # color of the series
		rp.append("chxl=0:|%s" % "|".join([mood[0].replace(" ", "%20") for mood in k_v]))

		r_plot = "&".join(rp)

	tagcloud = jhelpers.TagCloud(jmodels.Entry.objects.filter(\
		user__username=username),username)
	observer = jhelpers.Observer(username=username)
	searchform = jforms.SearchForm()

	return render_to_response('journal/summary.html', {'recent': summary_entries, \
		'tagcloud':tagcloud, 'observer':observer, 'radar_plot_options': r_plot, \
		'searchform': searchform}, context_instance=RequestContext(request))

"""
Journal page is just a listing of all entries the user has made
"""
def journal(request,username=None,year=None,month=None):

	today = date.today()

	username = username or request.user.username

	if year and month:
		year = int(year)
		month = int(month)
	else:
		year = today.year
		month = today.month

	entries = jmodels.Entry.objects.filter(user__username=username,date__year=year,date__month=month).order_by('-date')

	c = []
	grace_days = [today - timedelta(days=delta) for delta in range(4)]

	for week in calendar.monthcalendar(year,month):
		row = []

		for day in week:
			entry = None
			entry_grace_period = False

			if day > 0:
				try:
					entry = entries.get(date__day=day)
				except jmodels.Entry.DoesNotExist:
					if date(year,month,day) in grace_days:
						entry_grace_period = True

			row.append({'day':day,'entry':entry,'entry_grace_period': entry_grace_period})

		c.append(row)

	try:
		next_month = date(year,month+1,1)
	except ValueError:
		next_month = date(year+1,1,1)
	try:
		last_month = date(year,month-1,1)
	except ValueError:
		last_month = date(year-1,12,1)

	month_name = date(year,month,1).strftime("%B")

	return render_to_response('journal/entry_list.html',\
	{'calendar': c, 'month_name': month_name, 'month': month, 'year': year, 'next_month': next_month, 'last_month': last_month},\
	 context_instance=RequestContext(request))

def stats(request,username=None):
	form = jforms.DateForm(request.GET or None)

	username = username or request.user.username

	trend = jmodels.MoodTrend.objects.filter(username=username)
	entries = jmodels.Entry.objects.filter(user__username=username)

	if request.GET and form.is_valid() and form.cleaned_data.get('start'):
		dates = (form.cleaned_data.get('start'), form.cleaned_data.get('end'))
		trend = trend.filter(entrydate__range=dates)
		entries = entries.filter(date__range=dates)

	output = {}
	if trend.count():
		# {'mood': [(value,date),]}
		moods = {}
		for m in trend:

			if m.moodname not in moods:
				moods[m.moodname] = []

			moods[m.moodname].append((Decimal(m.value),m.entry.date))

		# get our mood avgs, this will build a bar graph in the html
		mood_avg_values = {}
		for moodname, values in moods.iteritems():
			value_total = 0
			for v in values:
				value_total += v[0]

			mood_avg_values[moodname] = value_total / len(values)

		# day of the week mood avg
		days = ({'day': 'monday', 'moods': {}},
				{'day': 'tuesday', 'moods': {}},
				{'day': 'wednesday', 'moods': {}},
				{'day': 'thursday', 'moods': {}},
				{'day': 'friday', 'moods': {}},
				{'day': 'saturday', 'moods': {}},
				{'day': 'sunday', 'moods': {}})

		for t in trend:
			day = t.entrydate.weekday()
			if t.moodname not in days[day]['moods']:
				days[day]['moods'].update({t.moodname: []})

			days[day]['moods'][t.moodname].append(Decimal(t.value))

		daily_moods = {}
		for d in days:
			for key,values in d['moods'].iteritems():
				if key not in daily_moods:
					daily_moods[key] = []
				daily_moods[key].append('%.2f' % (sum(values) / len(values)))
		daily_moods = [(k,v) for k,v in daily_moods.iteritems()]
		daily_moods.sort()

		"""
		# now that we have avgs, we can build the std deviation, showing whether or not someones mood changes drastically
		# we can even rate it based on how drastic the changes are, eg: 0-3 = low, 4-7 = med 7-10 = high (10 std deviation should be impossible)

		mood_deviation = {}
		for k,v in moods.iteritems():

			# for each value, we need to subtract the the mean from it, then square the value
			population_std_deviation = [(value-mood_avg_values[k])**2 for value in v]

			# take the sum and divide by the amount of values we have
			population_std_deviation = sum(population_std_deviation) / len(v)

			# the sqr root will give us our std deviation now for this mood
			mood_deviation[k] = "%.2f" % math.sqrt(population_std_deviation)
		"""

		mood_avg_deviation = {}
		for k,v in mood_avg_values.iteritems():
			mood_avg_deviation[k] = {'avg': "%.2f" % (v)}

		"""
		for k,v in mood_deviation.iteritems():
			mood_avg_deviation[k].update({'std': v})
		"""

		output = {
			'mood_avg_deviation': [(k,v) for k,v in mood_avg_deviation.iteritems()],
			'entries': entries,
			'mood_values': moods,
			'mood_per_day': daily_moods
		}
	return render_to_response('journal/stats.html', {'form': form, 'stats': output},
		context_instance=RequestContext(request))

def manage_tags(request):

	entries = jmodels.Entry.objects.filter(user=request.user)

	tags = {} # Dictionary of all tags used, where the key is the tag and the value is the number of times the tag is used

	for entry in entries:
		if entry.tags:
			for tag in entry.tags.split(","):
				t = tag.strip()
				if t not in tags:
					tags[t] = 1
				else:
					tags[t] += 1

	from operator import itemgetter
	tags = sorted(tags.iteritems(), key=itemgetter(1), reverse=True)

	return render_to_response('journal/tag_manager.html', {'tags':tags}, context_instance=RequestContext(request))

def entry_search(request, username=None):

	is_self = False
	if not username or username == request.user.username:
		username = request.user.username
		is_self = True

	results = jmodels.Entry.objects.filter(user__username=username)
	if not is_self:
		results = results.exclude(is_private=True)

	form = jforms.SearchForm(request.GET or None)
	if request.GET and form.is_valid():
		results = form.get_results(results)

	return render_to_response('journal/entry_search.html', {'form': form,
		'results': results}, context_instance=RequestContext(request))

