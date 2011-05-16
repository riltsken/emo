from django.db import models
from django.contrib.admin.models import User

from emo.tracker import choices

"""
A user creates a TrackGroup.
Example: Weight Loss TrackGrojup, Relationship TrackGroup

Within each TrackGroup, they create one or more Trackers.
Trackers are named and given a 'field' which determines how they are displayed.
A Tracker is then assigned a ValueToTrack.

Value objects determine what type of data the user is tracking.
It is these Value objects that the user will create several of, at whatever
interval they choose.
"""

class TrackGroup(models.Model):
	name = models.CharField(max_length=50)
	user = models.ForeignKey(User,editable=False)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.name

class Tracker(models.Model):
	group = models.ForeignKey('TrackGroup')
	label = models.CharField(max_length=50)
	field = models.CharField(max_length=50,choices=choices.FORM_TYPES)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.label
	
class ValueToTrack(models.Model):
	tracker = models.ForeignKey('Tracker',null=False,editable=False)
	date = models.DateTimeField()

	def __unicode__(self):
		return self.value

	class Meta:
		abstract = True

class ValueInteger(ValueToTrack):
	value = models.IntegerField(max_length=15)

class ValueDecimal(ValueToTrack):
	value = models.DecimalField(max_digits=20, decimal_places=5)

class ValueString(ValueToTrack):
	value = models.CharField(max_length=100)

class ValueText(ValueToTrack):
	value = models.TextField()

class ValueDateTime(ValueToTrack):
	value = models.DateTimeField()

class ValueBoolean(ValueToTrack):
	value = models.NullBooleanField()

class ValueOneRelation(ValueToTrack):
	value = models.ForeignKey('ValueKey')
	set = models.ForeignKey('ValueKeySet')

class ValueManyRelation(ValueToTrack):
	value = models.ManyToManyField('ValueKey')
	set = models.ForeignKey('ValueKeySet')

class ValueKey(models.Model):
	# Relations will link to these.
	name = models.CharField(max_length=50)
	value = models.CharField(max_length=100)
	set = models.ForeignKey('ValueKeySet')

class ValueKeySet(models.Model):
	name = models.CharField(max_length=50)
