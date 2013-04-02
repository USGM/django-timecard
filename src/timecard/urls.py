from django.conf.urls.defaults import *
from timecard.views import *

urlpatterns = patterns('timecard.views',
                       
    url(r'^my-time/$', my_time, name='my_time',),
    
    url(r'^admin/report/$', admin_upcoming_hours, name='hours',),
)
