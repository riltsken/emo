import os
from databases import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Alex',	'alexbmeng@gmail.com'),
     ('Sam',	'samueltoriel@gmail.com'),
)

MANAGERS = ADMINS

FILE_PATH = os.getcwd()

TIME_ZONE =		'US/Eastern'
LANGUAGE_CODE =	'en-us'
SITE_ID =		1
USE_I18N =		True

USE_CUSTOM_CSS = False
MEDIA_ROOT = '%s/media/' % FILE_PATH
MEDIA_URL			= '/media/'
ADMIN_MEDIA_PREFIX	= '/media/admin/'

SECRET_KEY = 't@v!va#zjj31vk!ly54hc0o#h@yjd4+&%l8v0nmc2@w(1_2vsu'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = [
	'django.core.context_processors.auth',
	'django.core.context_processors.media',
	'django.core.context_processors.request',
	'django.contrib.messages.context_processors.messages',
	'django.contrib.auth.context_processors.auth',
	'announcements.context_processors.announcements',
	'emo.userprofile.context_processors.profile',
	'emo.context_processors.viewing_friends_profile'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'emo.middleware.ExceptionExtraMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'announcements.middleware.AnnouncementsMiddleware',
	'emo.middleware.LoginRequired',
	'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'emo.urls'

TEMPLATE_DIRS = (
	'%s/templates/' % FILE_PATH
)

ACCOUNT_ACTIVATION_DAYS =	7
EMAIL_SUBJECT_PREFIX =		"[Emovolution] "
SERVER_EMAIL =				"no-reply-error@emovolution.com"
DEFAULT_FROM_EMAIL =		"no-reply@emovolution.com"
LOGIN_REDIRECT_URL =		"/"

INSTALLED_APPS = [
	'django.contrib.admin',
    'django.contrib.auth',
	'django.contrib.comments',
    'django.contrib.contenttypes',
	'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',

	'registration',
	'voting', # feedback
	'gravatar', # feedback
	'djangovoice', # used as our feedback app
	'compressor', # used to compress js/css
	'announcements', # used for sitewide announcements / summary page announcements

	'emo.userprofile',
	'emo.journal',
	'emo.social',
	'emo.moods',
	'emo.utils',
	'emo.tracker',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
CACHE_BACKEND = CACHES
