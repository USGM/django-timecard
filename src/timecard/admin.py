from django.contrib import admin
from django.contrib.auth import get_user_model
from timecard.models import Entry

User = get_user_model()

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = User.objects.filter(is_staff=True)
        return super(EntryAdmin, self).formfield_for_foreignkey(db_field,
            request, **kwargs)
admin.site.register(Entry, EntryAdmin)
