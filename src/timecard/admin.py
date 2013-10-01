from django.contrib import admin
from timecard.models import Entry

def mark_paid(modeladmin, request, queryset):
    """
    Marks a queryset of entries as paid.
    """
    queryset.update(status=Entry.PAID)

mark_paid.short_description = "Mark these entries as paid."

def mark_upcoming(modeladmin, request, queryset):
    """
    Marks a queryset of entries as upcoming.
    """
    queryset.update(status=Entry.UPCOMING)

mark_upcoming.short_description = "Mark these entries as uncoming."

class EntryAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'start_time', 'end_time', 'hours', 'status', )
    list_filter = ('status', 'user',)
    date_hierarchy = 'date'
    actions = [mark_paid, mark_upcoming]

admin.site.register(Entry, EntryAdmin)
