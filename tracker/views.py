from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect,HttpResponse,Http404
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext

from emo.tracker import forms as tforms
from emo.tracker import models as tmodels

def group_form(request,group_id=None):
	group = None
	if group_id:
		group = get_object_or_404(tmodels.TrackGroup, id=group_id)

	form = tforms.GroupForm(request.user, request.POST or None,instance=group)
	
	if request.POST and form.is_valid():
		group = form.save()
		if group_id:
			messages.success(request,"Your tracking group has been updated.")
		else:
			messages.success(request,"Your tracking group has been created.")
		return HttpResponseRedirect(reverse("tracker_group", args=[group.id,]))

	return render_to_response('tracker/group_form.html', {'form': form}, context_instance=RequestContext(request))

def group(request,group_id=None):
	group = get_object_or_404(tmodels.TrackGroup, id=group_id)
	return render_to_response('tracker/group.html', {'group': group}, context_instance=RequestContext(request))

def tracker_form(request,group_id=None,track_id=None):
	group = None
	tracker = None

	if group_id:
		group = get_object_or_404(tmodels.TrackGroup, id=group_id)
	if track_id:
		tracker = get_object_or_404(tmodels.Tracker, id=track_id)

	form = tforms.TrackerForm(group, request.POST or None,instance=tracker)

	if request.POST and form.is_valid():
		tracker = form.save()
		if tracker_id:
			messages.success(request,"Your tracker has been updated.")
		else:
			messages.success(request,"Your tracker has been created.")
		return HttpResponseRedirect(reverse("tracker_group", args=[group.id,]))

	return render_to_response('tracker/tracker_form.html', {'form': form}, context_instance=RequestContext(request))

def tracker_fillout(request,group_id=None,track_id=None):
	return render_to_response('tracker/tracker_fillout.html', {'form': form}, context_instance=RequestContext(request))

