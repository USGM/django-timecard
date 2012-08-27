from django.contrib import admin

from timecard.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('date', 'user', 'start_time', 'end_time', 'difference_hours_nice', 'status', )
	list_filter = ('user', 'status', )
	date_hierarchy = 'date'
	
	def difference_hours_nice(self, entry):
		hours = entry.difference_hours
		return round(hours, 2)

admin.site.register(Entry, EntryAdmin)