from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from timecard.models import Entry

def my_time(request):
    
    user = request.user
    
    upcoming_time = Entry.objects.filter(user=user, status=Entry.UPCOMING)
    
    paid_time = Entry.objects.filter(user=user, status=Entry.PAID)
    
    return render_to_response("my_timecard.html", 
                              {'upcoming_time': upcoming_time, 'paid_time': paid_time, }, 
                              context_instance=RequestContext(request))