from datetime import datetime

from django.db import models
from django.contrib.admin.models import User

from emo.userprofile import choices

"""
A user on emovolution has certain demographic information that we can use to produce trending charts from.

Anytime they save their profile, if any field changes, then a new profile is created in the database for them.
We always store previous profile information for reporting purposes, such as weight / industry / employment status.
"""
class BaseProfile(models.Model):
	
	user = models.ForeignKey(User,editable=False)
	created = models.DateTimeField(default=datetime.now,editable=False)

	# demographic information
	birthdate = models.DateField(blank=True,null=True)
	weight = models.PositiveIntegerField(blank=True,null=True,help_text="lbs (pounds)") # stored as pounds
	height = models.PositiveIntegerField(blank=True,null=True,help_text="in (inches)") # stored as inches
	gender = models.CharField(choices=choices.GENDER,max_length=1,blank=True,null=True)
	race = models.CharField(choices=choices.RACE,max_length=10,blank=True,null=True)
	education = models.CharField(choices=choices.EDUCATION,max_length=20,blank=True,null=True)
	employment = models.CharField(choices=choices.EMPLOYMENT_STATUS,max_length=20,blank=True,null=True)
	industry = models.CharField(choices=choices.INDUSTRY,max_length=20,blank=True,null=True)
	marital = models.CharField(choices=choices.MARITAL_STATUS,max_length=15,blank=True,null=True)
	sexual_orientation = models.CharField(choices=choices.ORIENTATION,max_length=10,blank=True,null=True)
	mbti = models.CharField(choices=choices.MBTI,max_length=4,blank=True,null=True,help_text="<span id='mbti-help' class='question-mark'>?</span>")
	extroversion = models.PositiveIntegerField(blank=True,null=True,help_text="A measurement of how extroverted you think you are.")
	income = models.CharField(choices=choices.INCOME_LEVEL,max_length=2,blank=True,null=True)

	# these are settings on a different page
	metric_system = models.CharField(choices=choices.METRICS,max_length=2,default="US")
	timezone = models.CharField(choices=choices.TIMEZONES,max_length=5,default="-5")
	date_display = models.CharField(choices=choices.DATEDISPLAY,max_length=15,default="mm/dd/yyyy")

	# this hides the entire profile, and supercedes the privacy field
	public = models.BooleanField(default=False)

	# comma-separated field names, whether or not they should be shown publicly
	privacy = models.TextField(editable=False,blank=True,null=True)

	# helps us determine if this is still a guest account
	is_guest = models.BooleanField(default=False,editable=False)

	# Override the != operator for these objects so we can just do old_profile != new_profile when checking whether we should
	# save or not
	def __ne__(self,other):
		fields = self._meta.get_all_field_names()
		fields.remove('id')
		fields.remove('created')
		fields.remove('user')
		for f in fields:
			if getattr(self,f) != getattr(other,f):
				return True
		return False
	
	class Meta:
		abstract = True

class Profile(BaseProfile):

	@staticmethod
	def create_history(profile):
		fields = profile._meta.get_all_field_names()
		fields.remove('id')
		attrs = {}
		for f in fields:
			attrs[f] = getattr(profile,f)

		HistoryProfile.objects.create(**attrs)

class HistoryProfile(BaseProfile):
	pass

# Signals
def create_history(sender,instance,**kwargs):
	if sender.objects.filter(user=instance.user).count():
		old_profile = sender.objects.get(user=instance.user)
		if old_profile != instance:
			Profile.create_history(instance)
	else:
		Profile.create_history(instance)

def new_user_profile(sender,instance,created,**kwargs):
	if created:
		Profile.objects.create(user=instance)
		HistoryProfile.objects.create(user=instance)
		
models.signals.post_save.connect(new_user_profile, sender=User)
models.signals.pre_save.connect(create_history, sender=Profile)

