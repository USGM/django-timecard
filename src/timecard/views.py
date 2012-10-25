from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

from timecard.models import Entry
from timecard import *
from datetime import *
from dateutil import *
from dateutil.relativedelta import *
from math import *

from warehouse.forms import DateRangeForm

import operator

def build_hours(iterable):
    
    total_hours = 0
    work_days = {}
    for entry in iterable:
        try:
            (date, entries, hours) = work_days[entry.date]
            entries.append(entry)
            hours += entry.hours
            total_hours += entry.hours
            work_days[entry.date] = (date, entries, hours)
        except KeyError:
            work_days[entry.date] = (entry.date, [entry, ], entry.hours)
            total_hours += entry.hours
            
    for date, (another_date, entries, hours) in work_days.iteritems():
        entries.sort(key=operator.attrgetter('start_time', 'id'))
        work_days[date] = (another_date, entries, hours)
            
    work_day_list = work_days.values()
    work_day_list.sort()
    
    
    hours_part = int(floor(total_hours))
    minutes_part = round((total_hours - hours_part)*60, 0)
    hours_and_minutes = "%d:%02d" % (hours_part, minutes_part)
    
    return work_day_list, total_hours, hours_and_minutes

def nearest_minute():
    """
    If you don't add 30 seconds then you're always truncating with an
    average loss of 30 seconds.  This makes it effectively rounding, in aggregate.
    Since it's only a single minute and since a person is just as likely
    to gain a minute as lose a minute, this is unbiased.
    The law of large numbers (of samples) starts to kick in around 25 samples for a normal distribution.
    One week of clocking in and out is 5*2*2 = 20 (including break or lunch) so by the time it's been two
    weeks the math says we're now unbiased.
    """
    now = datetime.now() + relativedelta(seconds=30)
    nearest_minute = time(now.hour, now.minute)
    return nearest_minute

@login_required
def my_time(request):
    
    if request.method == "POST":
        if "punch_in" in request.POST:
            if can_punch_in(request.user):
                new_entry = Entry(user=request.user, date=date.today(), start_time=nearest_minute())
                new_entry.save()
            else:
                messages.error(request, "You can't punch in yet since you have open entries")
            
        elif "punch_out" in request.POST:
            
            if can_punch_out(request.user):
                start_entry = Entry.objects.get(user=request.user, end_time=None)
                start_entry.end_time = nearest_minute()
                start_entry.save()
                
            else:
                empty_entries = Entry.objects.filter(user=request.user, end_time=None).order_by('-date')
            
                count = empty_entries.count()
                if count >= 1:
                    messages.error(request, "You can't punch out since there are %d punch-ins during the last 24 hours!" % count)
                    
                elif count <= 0:
                    messages.error(request, "You can't punch out since there isn't a punch-in during the last 24 hours!")
                    
                else:
                    messages.error(request, "I don't know what went wrong here!")
        
    
    user = request.user
    
    upcoming_days, upcoming_hours, upcoming_hours_minutes = build_hours(Entry.objects.filter(user=user, status=Entry.UPCOMING))
    
    paid_days, paid_hours, paid_hours_minutes = build_hours(Entry.objects.filter(user=user, status=Entry.PAID))
    
    return render_to_response("my_timecard.html", 
                              {
                               'upcoming_days': upcoming_days, 
                               'upcoming_hours': upcoming_hours,
                               'paid_days': paid_days, 
                               'paid_hours': paid_hours,
                               'can_punch_in': can_punch_in(request.user),
                               'can_punch_out': can_punch_out(request.user),
                               }, 
                              context_instance=RequestContext(request))

def build_employee_report(iterable):
    employees = {}
    
    report_list = []
    for entry in iterable:
        try:
            employees[entry.user].append(entry)
        except KeyError:
            employees[entry.user] = [entry, ]
            
            
    for user, entrylist in employees.iteritems():
        work_days, hours, hours_and_minutes = build_hours(entrylist)
        report_list.append((user, work_days, hours, hours_and_minutes))
        
    return report_list
        

@permission_required('timecard.change_entry')
def admin_upcoming_hours(request):
    upcoming_paychecks = Entry.objects.filter(status=Entry.UPCOMING)
    
    filter_form = DateRangeForm()
    
    if request.method == "POST":
        
        filter_form = DateRangeForm(request.POST)
        
        if filter_form.is_valid():
            upcoming_paychecks = upcoming_paychecks.filter(filter_form.get_query('date'))
            
            
    report_list = build_employee_report(upcoming_paychecks)
    
    return render_to_response("admin/timecards.html", 
                              {
                               'report_list': report_list,
                               'filter_form': filter_form,
                               }, 
                              context_instance=RequestContext(request))
    
    
    