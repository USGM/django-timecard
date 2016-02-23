import datetime

from dateutil import parser

from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms.widgets import Input


class TimeWidget(Input):
    format = '%I:%M %p' # '12:20 PM'

    def __init__(self, attrs=None, format=None):
        self.attrs = {'class': 'vTimeField', 'size': '8', 'autocomplete': 'off'}
        super(TimeWidget, self).__init__(self.attrs)
        if format:
            self.format = format

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''

        if hasattr(value, 'strftime'):
            value = value.strftime(self.format)

        return super(TimeWidget, self).render(name, value, attrs)


class FuzzyTimeField(forms.Field):
    widget = TimeWidget

    def clean(self, value):
        super(FuzzyTimeField, self).clean(value)
        if value in (None, ''):
            return None

        if isinstance(value, datetime.time):
            return value
        else:
            try:
                return parser.parse(value).time()
            except ValueError, e:
                raise ValidationError(u'Enter a valid date and time')


class TimecardForm(forms.Form):
    date = forms.DateField(label=u'Date', widget=forms.HiddenInput)
    time_in = FuzzyTimeField(label=u'Time in', required=True)
    lunch_out = FuzzyTimeField(label=u'Lunch out', required=False)
    lunch_in = FuzzyTimeField(label=u'Lunch in', required=False)
    time_out = FuzzyTimeField(label=u'Time out', required=False)

    fm_name = forms.CharField(widget=forms.HiddenInput, initial=u'TimecardForm')

BREAK_DURATION_CHOICES = (
    (5, '5 min'),
    (10, '10 min'),
    (15, '15 min'),
    (20, '20 min'),
    (30, '30 min'),
    (40, '40 min'),
    (50, '50 min'),
    (60, '1 hour'),
)


class BreakForm(forms.Form):
    duration = forms.ChoiceField(label=u'Duration', choices=BREAK_DURATION_CHOICES)
    fm_name = forms.CharField(widget=forms.HiddenInput, initial=u'BreakForm')


class DateRangeForm(forms.Form):
    """
    Search for items by date range.
    """
    from_date = forms.DateField()
    to_date = forms.DateField()

    def __init__(self, *args, **kwargs):
        """
        We aren't going to know what the defaults should be in all cases,
        so we derive them from the initial data in this hacky manner.
        """
        super(DateRangeForm, self).__init__(*args, **kwargs)
        from_date = u'from_date'
        to_date = u'to_date'
        if self.prefix:
            from_date = u'%s-from_date' % self.prefix
            to_date = u'%s-to_date' % self.prefix
        if from_date not in self.data:
            if u'from_date' in self.initial:
                self.data[from_date] = self.initial['from_date']
        if to_date not in self.data:
            if u'to_date' in self.initial:
                self.data[to_date] = self.initial['to_date']
        self.is_bound = True

    def get_from_date(self):
        temp = self.cleaned_data['from_date']
        from_date = datetime.datetime(temp.year, temp.month, temp.day, 0, 0, 0, 0)
        return from_date

    def get_to_date(self):
        temp = self.cleaned_data['to_date']
        to_date = datetime.datetime(temp.year, temp.month, temp.day, 23, 59, 59, 999999)
        return to_date

    def get_query(self, date_field):
        search_query = Q(id__gte=0)

        if self.is_valid():
            search_query &= Q(**{"%s__gte" % date_field: self.get_from_date()})
            search_query &= Q(**{"%s__lte" % date_field: self.get_to_date()})

        return search_query
