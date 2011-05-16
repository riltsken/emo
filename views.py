from django.conf import settings
from django.http import HttpResponse
from django import http
from django.template import Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context:
        MEDIA_URL
            Path of static media (e.g. "media.example.org")
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(Context({
        'MEDIA_URL': settings.MEDIA_URL
    })))

def announcement_archive(request):

	from datetime import datetime
	from django.shortcuts import render_to_response
	from django.template import RequestContext
	from announcements.models import Announcement as AN

	a = AN.objects.filter(start_time__lt=datetime.now()).order_by('-start_time')

	return render_to_response('announcement_archive.html',{'announcements': a},context_instance=RequestContext(request))

@csrf_exempt
def mobile_login(request):

	username = request.POST.get('username', None)
	password = request.POST.get('password', None)

	user = authenticate(username=username,password=password)
	if user:
		request.session.modified = True
		return HttpResponse("sessionid=%s" % request.session.session_key)
	return HttpResponse("False")

