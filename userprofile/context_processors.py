from emo.userprofile import models as upmodels

def profile(request):

	profile = None

	if request.user.is_authenticated():
		profile = request.user.profile_set.latest('created')

	return {'request_user_profile': profile}
