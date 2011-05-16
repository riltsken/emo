from decimal import Decimal

from django.contrib.admin.models import User
from django.db import models

from emo.moods.models import Mood

class Entry(models.Model):

	created = models.DateTimeField(editable=False) # this is the timestamp when they created it
	date = models.DateField(editable=False) # this is the actual date of the entry
	user = models.ForeignKey(User,editable=False)
	journal = models.TextField(null=True,blank=True)

	# Storing tags as foreign keys will lead to huge queries. Comma seperated is better.
	# Validate this field at the form level.
	tags = models.TextField(null=True,blank=True)

	is_private = models.BooleanField(default=False,verbose_name="Private entry")

	class Meta:

		verbose_name_plural = "Entries"
		ordering = ("-date", "user", )
		get_latest_by = "date"
		unique_together = ('date','user')

	def tag_list(self):

		return [t.strip() for t in self.tags.split(',')]

	def pretty_tags(self):

		tags = [t.strip() for t in self.tags.split(',')]
		return ', '.join(tags)

	def mood_avg(self):

		return "%.2f" % (self.moodtrend_set.aggregate(v=models.Sum('value'))['v'] / Decimal(self.moodtrend_set.count()))

class MoodTrend(models.Model):

	mood = models.ForeignKey(Mood)
	entry = models.ForeignKey(Entry)
	value = models.PositiveIntegerField(max_length=2) # form value should validate this as a value from 1-10

	# we can get this from the entry, but this saves a join
	username = models.CharField(max_length=200)
	entrydate = models.DateField()

	# TODO: make sure this value updates if mood.name changes
	moodname = models.CharField(max_length=50)

	class Meta:
		unique_together = ('mood','entry')
		ordering = ('mood__id',)

	def __unicode__(self):

		return "%s: %s" % (self.moodname, self.value)

