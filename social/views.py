from django.contrib import messages
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext

from emo.social import models as smodels
from emo.social import forms as sforms
from emo.userprofile import models as upmodels

def search(request,username=None):

	form = sforms.SearchForm(request.user)

	users = User.objects.filter(profile__is_guest=False,profile__public=True).exclude(pk=request.user.pk).order_by("username")
	relatives = smodels.Relationship.get_relatives(request.user)

	return render_to_response('social/search.html', {'form': form, 'users': users, 'relatives': relatives}, context_instance=RequestContext(request))

msg = { # A username should be appended to each message to complete it:
	# From 0 to 1
	'success_add': {
		'bookmarked':	'You have bookmarked ',
		'pending':		'A request to bookmark has been sent to ',
		'approved':		'You have approved the following user to bookmark you: ',
		'blocked':		'You have blocked ',
	},
	# From 1 to 0
	'success_remove': {
		'bookmarked':	'You have unbookmarked ',
		'pending':		'A request to bookmark has been retracted from ',
		'approved':		'You have unapproved the following user to bookmark you: ',
		'blocked':		'You have unblocked ',
	},
	# From 1 to 1
	'dup_add': {
		'bookmarked':	'You have already bookmarked ',
		'pending':		'You have already requested to follow ',
		'approved':		'You have already approved ',
		'blocked':		'You have already blocked ',
	},
	# From 0 to 0
	'dup_remove': {
		'bookmarked':	'You cannot bookmark ',
		'pending':		'There is no request to remove from ',
		'approved':		'You do not have a pending request from ',
		'blocked':		'You have not blocked ',
	},
}

def edit_relationship(request,field="bookmarked",value=1):
	# fields can be: bookmarked, approved, pending, blocked.
	# value signifies what to change the value to.

	if request.GET.get('user'):
		host = request.user

		try:
			relative = User.objects.get(username=request.GET['user'])
		except User.DoesNotExist:
			messages.warning(request,"The requested user does not exist.")
		else:
			if relative == host:
				messages.warning(request, "Cannot perform this action on yourself.")
			else:
				relationship = smodels.Relationship.objects.get_or_create(host=host,relative=relative)[0]
				cr = smodels.Relationship.objects.get_or_create(host=relative, relative=host)[0] #Counter-relationship
				if getattr(relationship, field) == value == 1 and field != "pending":
					messages.warning(request, msg['dup_add'][field] + str(relative))
				elif getattr(relationship, field) == value == 0 and field != "pending":
					messages.warning(request, msg['dup_remove'][field] + str(relative))
				else:
					public_relative = relative.profile_set.get().public
					#Some specific checks here to make sure these changes are ok:
					errors = False

					if field == "bookmarked" and value == 1 and not public_relative:
						errors = True # I want to bookmark a private user
						messages.warning(request, "You cannot bookmark private users.")

					if field == "pending" and value == 1 and cr.blocked:
						errors = True # I want to request to follow someone who has blocked me
						messages.success(request, msg['success_add'][field] + str(relative)) # Pretend the request went through

					if field == "approved" and not relationship.pending:
						errors = True # I want to approve someone to follow me who has not asked to
						messages.warning(request, "%s has not requested to follow you." % relative)

					if not errors:
						if field == "pending":
							setattr(cr, field, value)
							cr.save()
						else:
							if field == "approved" and value == 1:
								relationship.pending = 0
								relationship.blocked = 0
							if field == "blocked" and value == 1:
								relationship.pending = 0
								relationship.blocked = 0

							setattr(relationship, field, value)
							relationship.save()
						if value == 1:
							messages.success(request, msg['success_add'][field] + str(relative))
						elif value == 0:
							messages.success(request, msg['success_remove'][field] + str(relative))

	return HttpResponseRedirect(request.GET.get('redirect', None) or reverse("social_list"))

def view_relatives(request):
	relatives = smodels.Relationship.objects.filter(host=request.user)

	bookmarked = relatives.filter(bookmarked=True)
	blocked = relatives.filter(blocked=True)
	requests = relatives.filter(pending=True, blocked=False)
	approved = relatives.filter(approved=True)

	pending = smodels.Relationship.objects.filter(relative=request.user,pending=True)

	if not relatives:
		messages.warning(request, "You do not currently have anyone bookmarked.")
		return HttpResponseRedirect(reverse("social_search"))

	return render_to_response('social/view.html', {'bookmarked': bookmarked, 'blocked': blocked, 'requests': requests, 'approved': approved, 'pending': pending}, context_instance=RequestContext(request))
