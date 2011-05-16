import re

USER_URL_REGEX = re.compile('/u/(?P<username>\w+)/.*')

def viewing_friends_profile(request):

	if USER_URL_REGEX.match(request.path):
		match = USER_URL_REGEX.match(request.path)

		username = match.groupdict()['username']

		viewing_self = True
		if request.user.is_authenticated() and username != request.user.username:
			viewing_self = False

		return {'viewing': {'self': viewing_self, 'username': username}}

	return {'viewing': {'self': True, 'username': None}}
