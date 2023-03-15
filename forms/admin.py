from django.contrib import admin

from .models import *

# Register your models here.


def readonly_change_fields(model_admin, request, obj):
    if obj:
        return model_admin.readonly_fields
    return []


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name', 'is_tech_event', 'schedule',
                    'is_team_event', 'min_team_members', 'max_team_members',
                    'is_registration_open')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'upi_reference_number')
    readonly_fields = ('event', 'upi_reference_number')

    def get_readonly_fields(self, request, obj=None):
        return readonly_change_fields(self, request, obj)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_name', 'email', 'mobile', 'is_registrant',
                    'event_name', 'team_id')
    readonly_fields = ('member_name', 'email', 'mobile',
                       'university_name', 'course_name', 'residence_area',
                       'is_registrant')

    def get_readonly_fields(self, request, obj=None):
        return readonly_change_fields(self, request, obj)

    def event_name(self, obj):
        return obj.team.event


admin.site.register(Updates_mail_list)
