from django.contrib import admin

from timecard.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('date', 'user', 'start_time', 'end_time', 'difference_hours')
	list_filter = ('user',)
	date_hierarchy = 'date'
	
	def difference_hours(self, entry):
		hours = float(entry.difference) / 3600.0
		return "0.00f" % (hours, )

admin.site.register(Entry, EntryAdmin)