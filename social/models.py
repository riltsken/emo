from django.contrib.admin.models import User
from django.db import models

class Relationship(models.Model):
	"""
	A Relationship object stores data about how a user (the 'host') sees another user (the 'relative').
	
	User A will have a table explaining his relationship with User B,
	while User B will have a seperate, unrelated table about User A.
	"""

	host = models.ForeignKey(User, editable=False, related_name="host") # The user
	relative = models.ForeignKey(User, related_name="relative")			# The person they are relating to
	bookmarked = models.BooleanField(default=False)						# Is the host following the relative (bookmarked)?
	approved = models.BooleanField(default=False)						# May the relative follow the private host (bookmark)?
	pending = models.BooleanField(default=False)						# Is there a pending request for the relative to follow the host?
	blocked = models.BooleanField(default=False)						# Has the host blocked the relative from requesting to follow?
	notes = models.TextField()											# Notes that the host stores about the relative

	def __unicode__(self):
		return "Relationship between %s and %s" % (str(self.host.username), str(self.relative.username))
	
	def reverse_relation(self):
		return Relationship.objects.get_or_create(host=self.relative,relative=self.host)[0]

	@staticmethod
	def get_relatives(user):
		# Return a list of all relatives of the given host user
		return User.objects.filter(relative__host=user).distinct()
