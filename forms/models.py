from django.conf import settings
from django.db import models
from tech_kaushalya import custom_fields

# Create your models here.


class Updates_mail_list(models.Model):
    email = custom_fields.LowerEmailField(
        unique=True,
        error_messages={
            'unique': 'Email already registered.',
            'blank': 'Email cannot be blank.'
        },
    )


class Event(models.Model):
    event_name = custom_fields.LowerCharField(
        max_length=30,
        unique=True,
        error_messages={
            'unique': 'An event with that name already exists.'
        }
    )
    is_tech_event = models.BooleanField()
    img = models.ImageField(
        upload_to='event_images/'
    )
    schedule = models.DateTimeField()
    registration_fee = models.PositiveSmallIntegerField()
    is_team_event = models.BooleanField()
    min_team_members = models.PositiveSmallIntegerField(default=1)
    max_team_members = models.PositiveSmallIntegerField(default=1)


class Team(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)


class Member(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    member_name = custom_fields.LowerCharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = custom_fields.LowerEmailField()
    is_registrant = models.BooleanField(default=False)


class Payment(models.Model):
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
