from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'is_tech_event', 'schedule', 'is_team_event', 'min_team_members', 'max_team_members')


admin.site.register(Updates_mail_list)
admin.site.register(Team)
admin.site.register(Member)
admin.site.register(Payment)
