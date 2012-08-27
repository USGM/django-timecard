from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

from timecard.models import Entry

def build_hours(queryset):
    work_days = {}
    for entry in queryset:
        try:
            (date, entries, hours) = work_days[entry.date]
            entries.append(entry)
            hours += entry.hours
            work_days = (date, entries, hours)
        except KeyError:
            work_days[entry.date] = (entry.date, [entry, ], entry.hours)
            
    for date, (another_date, entries, hours) in work_days.iteritems():
        entries.sort(key=lambda x: x.start_time)
            
    return work_days.values().sort(key=lambda x: x[0].date)

def my_time(request):
    
    user = request.user
    
    upcoming_time = build_hours(Entry.objects.filter(user=user, status=Entry.UPCOMING))
    
    paid_time = build_hours(Entry.objects.filter(user=user, status=Entry.PAID))
    
    return render_to_response("my_timecard.html", 
                              {'upcoming_time': upcoming_time, 'paid_time': paid_time, }, 
                              context_instance=RequestContext(request))