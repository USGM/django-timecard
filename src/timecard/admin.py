from django.contrib import admin
from decimal import Decimal
from timecard.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('date', 'user', 'start_time', 'end_time', 'difference_hours_nice', 'status', )
	list_filter = ('status', 'user',)
	date_hierarchy = 'date'
	
	def difference_hours_nice(self, entry):
		hours = entry.difference_hours
		return Decimal("%0.2f" % (round(hours, 2), ))

admin.site.register(Entry, EntryAdmin)