from django.conf.urls.defaults import *

urlpatterns = patterns('timecard.views',
                       
    url(r'^my-time/$', my_time, name='timecard.my_time',),
)
