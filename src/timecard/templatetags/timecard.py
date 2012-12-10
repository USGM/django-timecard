from django import template
from math import *

register = template.Library()


@register.tag
def display_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, hours = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    
    if not hours:
        raise template.TemplateSyntaxError("%r tag's argument needs to exist" % tag_name)
    return DisplayTime(template.Variable(hours))

class DisplayTime(template.Node):
    def __init__(self, hours):
        #print item_list
        self.hours = hours
    def render(self, context):
        try:
            actual_hours = self.hours.resolve(context)
            hours_part = int(floor(actual_hours))
            minutes_part = round((actual_hours - hours_part)*60, 0)
            hours_and_minutes = "%d:%02d" % (hours_part, minutes_part)
            return hours_and_minutes
        
        except template.VariableDoesNotExist:
            return ''