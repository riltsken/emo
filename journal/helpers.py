import random
from datetime import datetime, timedelta, date
from calendar import Calendar
from decimal import Decimal

from django.db.models import Avg
from django.core.urlresolvers import reverse

from emo.journal import models as jmodels
from emo.userprofile import models as upmodels
from emo.moods import models as mm

def range_of_date_week(d):
	#Change the date to the Monday of that week,and then append the next 6 days
	d = d - timedelta(d.weekday())
	range = []
	count = 0
	while count <= 6:
		range.append(d + timedelta(days=count))
		count += 1
	return range

"""
This is our mood analyzer

To add new moods, look at the get_blurbs method and add the method to the choices dictionary

format of different methods:

choices = {
	'title for blurb 1': {
		'option_1_for_blurb': (method, kwargs_for_method)
		'option_2_for_blurb': method_no_kwargs
	},
	'title for blurb 2': method
}

I kind of want to move all the blurb methods to another file so that the Observer class is cleaner and easier to read, we'll see
"""
class Observer:

	def __init__(self,username):
		
		self.username = username
		self.profile = upmodels.Profile.objects.filter(user__username=username).select_related('user').latest('created')
		self.has_entries = jmodels.Entry.objects.filter(user__username=username).count() > 0 # if they don't have entries this changes the blurbs

		if self.has_entries:
			self.week = (date.today() - timedelta(days=7), date.today())
			self.prev_week = (self.week[0] - timedelta(days=8), self.week[0] - timedelta(days=1))
			self.month = (date.today() - timedelta(days=30), date.today())
			self.prev_month = (self.month[0] - timedelta(days=30), self.month[0] - timedelta(days=1))

			has_monthly_entries = jmodels.Entry.objects.filter(user__username=username,date__range=(self.prev_month[0],self.month[1])).count() > 5
			has_weekly_entries = jmodels.Entry.objects.filter(user__username=username,date__range=(self.prev_week[0],self.week[1])).count() > 0

			self.period_choices = ['all']
			if has_monthly_entries:
				self.period_choices.append('month')
			if has_weekly_entries:
				self.period_choices.append('week')

			self.choices = self.get_choices()

	def get_blurbs(self):
		
		blurbs = []
		if not self.has_entries:
			blurbs = self.starter_blurbs()
		else:
			choices = random.sample(self.choices.values(), 5)

			for c in choices:
		
				if not isinstance(c, dict): # it is a method, there are no options meaning there is no week,month,all
					message = c()
				else:
					period = random.choice(c.keys())
		
					try:
						func,kwargs = c[period]
						message = func(**kwargs)
					except TypeError: # if there are not any kwargs
						func = c[period]
						message = func()
					
				blurbs.append(message)

		blurbs.insert(0,self.happy_birthday())
		if self.profile.is_guest:
			blurbs.append("<span class='bold'>If you want to keep this account you might want to activate it by going <a href='%s'>HERE</a></span>" % reverse('demo_activate')) 
		return blurbs

	def starter_blurbs(self):
		blurbs = []
		blurbs.append("Hey! Looks like you just started on Emovolution, lets get you going. ")
		blurbs.append("What you are looking at right now is the Summary Page, once you begin journaling things will fill up.")
		blurbs.append("You should start out by editing your profile <a href='%s'>HERE</a>" % reverse("profile_edit"))
		blurbs.append("Once you got that setup, you can browse your journals <a href='%s'>HERE</a>" % reverse("journal"))
		blurbs.append("We limit entries from today plus 3 days prior, since after that length of time one probably won't remember how they felt that day.") 

		return blurbs

	def get_choices(self):

		choices = {
			'Single mood': {
				'week': (self.compare_single_mood, {'period': self.week,'prev_period': self.prev_week}),
				'month': (self.compare_single_mood, {'period': self.month, 'prev_period': self.prev_month}),
				'all': self.compare_single_mood
			},

			'All moods': {
				'week': (self.compare_all_moods, {'period': self.week, 'prev_period': self.prev_week}),
				'month': (self.compare_all_moods, {'period': self.month, 'prev_period': self.prev_month}),
				'all': self.compare_all_moods
			},
			
			'Posting time of day': {
				'week': (self.compare_time_of_post, {'period': self.week}),
				'month': (self.compare_time_of_post, {'period': self.month}),
				'all': self.compare_time_of_post
			},

			'Post count possible': {
				'week': (self.post_count_possible, {'period': self.week}),
				'month': (self.post_count_possible, {'period': self.month}),
				'all': self.post_count_possible
			},

			'Lapse in posting': self.lapse_in_posts,
			'Post count': self.post_count,
			'Tag mood': self.compare_tag_mood
		}
		return choices

	def compare_single_mood(self,period=None,prev_period=None):
		
		mood = random.choice(mm.Mood.objects.filter(user__username=self.username,is_active=True\
			).values_list('name',flat=True))
		
		if period:
			current_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__range=period,moodname=mood).aggregate(v=Avg('value'))['v']
			prev_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__range=prev_period,moodname=mood).aggregate(v=Avg('value'))['v']
		else:
			current_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__range=self.week,moodname=mood).aggregate(v=Avg('value'))['v']
			prev_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__lt=self.week[0],moodname=mood).aggregate(v=Avg('value'))['v']

		trend = "risen"
		if current_mood > prev_mood:
			trend = "fallen"
		
		timeframe = "overall"
		if period:
			timeframe = "in the past month"
			if (period[1] - period[0]).days < 15: # subtract our dates just to see if its less than a month
				timeframe = "in the past week"
						
		return "Average for %s has %s %s." % (mood, trend, timeframe)

	def compare_all_moods(self,period=None,prev_period=None):
		
		if period:
			current_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__range=period).values('moodname','value')
			prev_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__range=prev_period).values('moodname','value')
		else:
			current_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__range=self.week).values('moodname','value')
			prev_mood = jmodels.MoodTrend.objects.filter(username=self.username,entrydate__lt=self.week[0]).values('moodname','value')


		# [{'moodname': "Happiness", 'value': 5.0},{},{}]
		cmood = {} # current mood
		for mood in current_mood:
			if mood['moodname'] not in cmood.keys():
				cmood[mood['moodname']] = []
			cmood[mood['moodname']].append( mood['value'] )
		for k,v in cmood.iteritems():
			cmood[k] = sum(cmood[k]) / Decimal(len(cmood[k])) # turn the list into an avg for the mood
		cmood_avg = sum(cmood.values()) / (Decimal(len(cmood.values())) or 1)

		pmood = {} # previous mood
		for mood in prev_mood:
			if mood['moodname'] not in pmood.keys():
				pmood[mood['moodname']] = []
			pmood[mood['moodname']].append( mood['value'] )
		for k,v in pmood.iteritems():
			pmood[k] = sum(pmood[k]) / Decimal(len(pmood[k])) # turn the list into an avg for the mood
		pmood_avg = sum(pmood.values()) / (Decimal(len(pmood.values())) or 1)
			 
		trend = "risen"
		if cmood_avg < pmood_avg:
			trend = "fallen"
		
		timeframe = "overall"
		if period:
			timeframe = "in the past month"
			if (period[1] - period[0]).days < 15: # subtract our dates just to see if its less than a month
				timeframe = "in the past week"
		
		return "Average mood has %s %s." % (trend, timeframe)

	def compare_tag_mood(self):
		
		current_mood = jmodels.Entry.objects.filter(user__username=self.username,date__range=(date.today() - timedelta(days=12), date.today()))
		prev_mood = jmodels.Entry.objects.filter(user__username=self.username)

		current_cloud = TagCloud(current_mood,self.username)
		prev_cloud = TagCloud(prev_mood,self.username)
		
		current_tags = current_cloud.ultimate_tag_dict()
		prev_tags = prev_cloud.ultimate_tag_dict()

		try:
			try_these_tags = random.sample(current_tags.keys(), 10)
		except ValueError:
			try_these_tags = current_tags.keys()
			random.shuffle(try_these_tags)

		for t in try_these_tags:
			
			ptag = prev_tags[t]
			ctag = current_tags[t]
			if ptag['count'] != ctag['count']:
				pmood = sum(ptag['avg_moods_raw'].values()) / len(ptag['avg_moods_raw'].values()) 	
				cmood = sum(ctag['avg_moods_raw'].values()) / len(ctag['avg_moods_raw'].values())
				if cmood > pmood:
					return "Your mood for the tag \'%s\' has risen" % t
				return "Your mood for the tag \'%s\' has fallen" % t

	def compare_time_of_post(self,period=None):
		pass

	def post_count_possible(self,period=None):

		if period == 'week':
			calendar_week = range_of_date_week(date.today())
			interval = (calendar_week[0], calendar_week[-1])
			completed = jmodels.Entry.objects.filter(user__username=self.username,date__range=interval).count()
			total_possible = 7
			return "Completed %s out of the %s possible journal entries this week" % (completed, total_possible)
		elif period == 'month':
			c = Calendar(0)
			weeks = c.monthdayscalendar(date.today().year,date.today().month)
			max_days = 1
			for w in weeks:
				max_days = max(w)
			completed = jmodels.Entry.objects.filter(user__username=self.username,date__year=date.today().year,date__month=date.today().month).count()
			total_possible = max_days
			return "Completed %s out of the %s possible journal entries this month" % (completed, total_possible)
		else:
			completed = jmodels.Entry.objects.filter(user__username=self.username).count()
			total_possible = (date.today() - self.profile.user.date_joined.date()).days + 4
			return "Completed %s out of the %s possible entries since you started journaling on Emovolution." % (completed, total_possible)

	def lapse_in_posts(self,period=None):

		perid = ['week','month']

		if period == 'week':
			current_mood = jmodels.Entry.objects.filter(user__username=self.username,date__range=self.week)
		else:
			current_mood = jmodels.Entry.objects.filter(user__username=self.username,date__range=self.month)

	def post_count(self):
		
		post_intervals = [5,10,15,30,45,60,90,120,150,200,250,300,400]
		posts = jmodels.Entry.objects.filter(user__username=self.username).count()
	
		if posts == 1:
			return "Congratulations! You made your first journal entry on Emovolution :)"

		for x,pcount in enumerate(post_intervals):
			if posts < pcount and posts > post_intervals[x-1]:
				return "You have written over %s journal entries on Emovolution!" % post_intervals[x-1]

	def happy_birthday(self):
		
		if self.profile.birthdate and (self.profile.birthdate.month, self.profile.birthdate.day) == (date.today().month, date.today().day):
			return "Happy birthday %s!" % (profile.user.username)

		return None	

class TagCloud:
	
	def __init__(self,query,username):

		self.username = username
		self.has_tags = any(query.values_list('tags',flat=True)) # used for questioning to print in template or not
		self.raw_tags = query.values_list('date','tags')

		self.frequency = self._get_frequency() # dict of tag,count (k,v)
		self.recent_tags = self._get_recency() # used for suggesting tags
		self.tag_mood = self._get_mood_per_tag() # we want the avg of each mood per tag rendered for the summary

		# used for cloud
		self.set_of_frequency = set(sorted(self.frequency.values()))
		self.length_of_frequency_set = len(self.set_of_frequency)
		self.set_tag_sizes()

	def _get_frequency(self):

		tag_frequency = {}
		for r in self.raw_tags:
			if r[1]:
				for t in r[1].split(','):
					if t:
						tag = t.strip()
						if tag_frequency.get(tag, None):
							tag_frequency[tag] += 1
						else:
							tag_frequency[tag] = 1

		return tag_frequency
	
	def _get_recency(self):
		
		tag_recency = {}
		for r in self.raw_tags:
			if r[1]:
				for t in r[1].split(','):
					if t:
						tag = t.strip()
						if tag_recency.get(tag, None) and tag_recency.get(tag, None) > r[0]:
							pass
						else:
							tag_recency[tag] = r[0]

		return tag_recency

	def _get_mood_per_tag(self):
		
		try: # If raw tags is an empty list, a max/min ValueError exception will be thrown, catch it and just return {} if that happens.
			max_date = max(self.raw_tags)[0]
			min_date = min(self.raw_tags)[0]
			

			moods = jmodels.MoodTrend.objects.filter(entrydate__range=(min_date,max_date),username=self.username).values('entrydate','moodname','value')

			# we are trying to build a dictionary that looks like this {'2010-10-01': {'value': 5, 'moodname': "Happiness", 'tags': []}, '2010-10-02': {}}
			tagmoods = []
			for m in moods:
				for entrydate,tags in self.raw_tags:
					if m['entrydate'] == entrydate and tags:
						tagmoods.append({
							'value': Decimal(m['value']),
							'moodname': m['moodname'],
							'tags': [t.strip() for t in tags.split(',') if t]
						})
			mood_per_tag = {}
			for tagmood in tagmoods:
				for tag in tagmood['tags']:
					if not mood_per_tag.get(tag, None):
						mood_per_tag[tag] = {tagmood['moodname']: [tagmood['value']]}
					else:
						if not mood_per_tag[tag].get(tagmood['moodname'], None):
							mood_per_tag[tag].update({tagmood['moodname']: [tagmood['value']]})
						else:
							mood_per_tag[tag][tagmood['moodname']].append(tagmood['value'])
		
			for tag,moods in mood_per_tag.iteritems():
				for mood,v in moods.iteritems():
					mood_per_tag[tag][mood] = sum(v) / len(v)
			return mood_per_tag

		except ValueError:
			return {}
	"""
	We have a max size of 40
	we have 7 diff tag amounts aka intervals
	40 / 7 = 4 which is the amount of difference between each size
	"""
	def set_tag_sizes(self,max_size=40,min_size=8):
		
		interval = 30 / ((self.length_of_frequency_set) or 1) # fallback for divide by 0
		size = min_size
		tag_sizes = {}
		for t in self.set_of_frequency:
			size += interval
			tag_sizes[t] = size
		
		self.tag_sizes = tag_sizes


	def ultimate_tag_dict(self):

		tag_dict = {}		
		for k,v in self.frequency.iteritems():
			tag_dict[k] = {'count': v, 'size': self.tag_sizes[v]}
		for k,v in self.tag_mood.iteritems():
			tag_dict[k].update({
				'avg_moods_raw': v,
				'avg_moods': dict([(mood,"%.2f" % decimal) for mood,decimal in v.iteritems()])
			})
		return tag_dict	
	
	def suggested_tags(self):
		
		frequent = [(v,k) for k,v in self.frequency.items()]
		frequent = sorted(frequent)[-5:]

		recent = [(v,k) for k,v in self.recent_tags.items()]
		recent = sorted(recent)[-5:]

		suggested_tags = set([r[1] for r in recent if r[1] != ""]) | set([f[1] for f in frequent if f[1] != ""])

		return suggested_tags
		
