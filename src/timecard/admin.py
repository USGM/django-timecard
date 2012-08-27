from django.contrib import admin

from timecard.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('date', 'user', 'start_time', 'end_time', 'difference_hours')
	list_filter = ('user',)
	date_hierarchy = 'date'
	
	def difference_hours(self, entry):
		return float(entry.difference) / 60.0

admin.site.register(Entry, EntryAdmin)