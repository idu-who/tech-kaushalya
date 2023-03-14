from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'is_tech_event', 'schedule',
                    'is_team_event', 'min_team_members', 'max_team_members',
                    'is_registration_open')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'event')

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_name', 'email', 'mobile', 'is_registrant',
                    'event_name', 'team_id')

    def event_name(self, obj):
        return obj.team.event

admin.site.register(Updates_mail_list)
admin.site.register(Payment)
