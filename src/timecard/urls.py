from django.conf.urls.defaults import *

urlpatterns = patterns('timecard.views',
                       
    url(r'^my-time/$', view_items, name='view-items',),
)
