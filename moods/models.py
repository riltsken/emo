from django.db import models
from django.contrib.admin.models import User

class Mood(models.Model):

	user = models.ForeignKey(User)	
	name = models.CharField(max_length=50)
	is_active = models.BooleanField(default=True)
	
	def __unicode__(self):

		return self.name

	class Meta:
	
		unique_together = ('user','name')
		ordering = ('id',)

def default_moods(sender,instance,created,**kwargs):
	if created:
		for mood in ['Happiness', 'Energy', 'Confidence', 'Peace of mind', 'Hope']:
			Mood.objects.create(user=instance,name=mood)

models.signals.post_save.connect(default_moods, sender=User)
	
