from django.conf.urls.defaults import *

urlpatterns = patterns('timecard.views',
	url(r'^(?P<username>[-\w]+)/(?P<year>\d{4})/(?P<week>\d{2})/$',
		view = 'weekly',
		name = 'timecard_weekly',
	),
	url(r'^$',
		view = 'index',
		name = 'timecard_homepage',
	),
)