import re
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.core.urlresolvers import reverse

from emo.userprofile import models as upmodels
from emo.social import models as smodels

USER_URL_REGEX = re.compile('/u/(?P<username>\w+)/')

PUBLIC_URL_REGEX = [
	re.compile('/account/.*$'),
	re.compile('/announcements/.*$'),
	re.compile('/media/.*$'),
	re.compile('/m/.*$'),
	re.compile('/about/'),
	re.compile('/terms/'),
	re.compile('/privacy/'),
	re.compile('/demo/'),
]

class LoginRequired:

	def process_view(self, request, view_func, view_args, view_kwargs):
		if request.user.is_authenticated():
			redirect = request.META.get('HTTP_REFERER', reverse('summary'))
			if 'emovolution' not in redirect:
				redirect = reverse('main')
		else:
			redirect = reverse('main')

		# permission check for /u/username/ path
		if USER_URL_REGEX.match(request.path):
			username = USER_URL_REGEX.match(request.path).groupdict()['username']

			# well if they request user is the same as the username... let them
			# continue
			if request.user.is_authenticated() and request.user.username == username:
				return

			# snatch the profile of the person we are supposed to be looking at since we'll be using it for a few checks.
			try:
				profile = upmodels.Profile.objects.filter(user__username=username).select_related('user').latest('created')
			except upmodels.Profile.DoesNotExist:
				messages.info(request,"Could not locate profile. Either it does not exist or it is set to private.")
				return HttpResponseRedirect(redirect)

			if not request.user.is_authenticated() or request.user.username != username:

				# a public profile means anyone can view it
				if profile.public:
					return

				# these must be private profiles after this point, so do the appropriate checks
				if request.user.is_authenticated():

					# check the approved list of the user we are looking at
					# if the user is approved to view their profile, go ahead and
					# let them continue.
					if smodels.Relationship.objects.filter(host__username=username,
						relative=request.user,approved=True).count():
						return

					# check the block list of the user we are looking at, and
					# stop anyone who is on that list.
					if smodels.Relationship.objects.filter(host__username=username,
						relative=request.user,blocked=True).count():
						messages.info(request,"Could not locate profile. Either it does not exist or it is set to private.")
						return HttpResponseRedirect(redirect)

				# Anyone who was able to view them was given the
				# ability to do so above. Block 'em
				if not profile.public:
					messages.info(request,"Could not locate profile. Either it does not exist or it is set to private.")
					return HttpResponseRedirect(redirect)

			# looks like we are ok to view it!
			return

		if request.user.is_authenticated():
			return

		if request.path == '/':
			return

		for public_url in PUBLIC_URL_REGEX:
			if public_url.match(request.path):
				return

		messages.warning(request,"You must be logged in to perform that action")
		return HttpResponseRedirect(reverse('main'))

class ExceptionExtraMiddleware(object):
	def process_exception(self, request, exception):
		if settings.DEBUG:
			return
		try:
			logged_in_info = ''
			if request.user and request.user.is_authenticated():
				logged_in_info = "%s" % request.user
				if request.user.email:
					logged_in_info += ' %s' % request.user.email
				if request.user.first_name or request.user.last_name:
					logged_in_info += ' (%s %s)' % (request.user.first_name, request.user.last_name)
			if logged_in_info:
				request.META['LOGGED-IN-USER'] = logged_in_info
		except:
			# don't make matters worse in these sensitive times
			logging.debug("Unable to debug who was logged in", exc_info=True)

