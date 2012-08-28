import datetime
from decimal import Decimal

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from timecard.managers import EntryManager

class Entry(models.Model):
	"""A Timecard Entry."""
	
	UPCOMING = 1
	PAID = 100
	
	ENTRY_STATUSES = (
		(UPCOMING, 'Upcoming'),
		(PAID, 'Paid'),
	)
	
	date = models.DateField()
	
	start_time = models.TimeField()
	end_time = models.TimeField(blank=True, null=True)
	
	user = models.ForeignKey(User)
	
	status = models.IntegerField(choices=ENTRY_STATUSES, default=UPCOMING)
	
	objects = EntryManager()
	
	class Meta:
		verbose_name = _('entry')
		verbose_name_plural = _('entries')
		db_table = 'timecard_entries'
		get_latest_by = 'date'
		ordering = ('-date', '-start_time')
	
	def __unicode__(self):
		if self.end_time:
			return u"%s: %s-%s" % (self.date.isoformat(), self.start_time.isoformat(), self.end_time.isoformat())
		else:
			return u"%s: %s" % (self.date.isoformat(), self.start_time.isoformat())
		
	def summary(self):
		if self.end_time:
			return u'%s to %s' % (self.start_time.strftime("%H:%M"), self.end_time.strftime("%H:%M"))
		else:
			return u'%s to ? ' % (self.start_time.strftime("%H:%M"), )
	
	@property
	def difference(self):
		if self.end_time:
			diff = datetime.datetime.combine(self.date, self.end_time) - datetime.datetime.combine(self.date, self.start_time)
		else:
			diff = datetime.datetime.now() - datetime.datetime.combine(self.date, self.start_time)
		
		return float(diff.seconds)
	
	@property
	def hours(self):
		hours = self.difference / 3600.00
		return Decimal("%0.2f" % (round(hours, 2), ))
		