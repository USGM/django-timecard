

from models import Entry



def can_punch_in(user):
    non_closed = Entry.objects.filter(user=user, end_time=None)
    return non_closed.count() == 0
    
def can_punch_out(user):
    non_closed = Entry.objects.filter(user=user, end_time=None)
    return non_closed.count() == 1