from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
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

    def __str__(self):
        return self.email


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
    min_team_members = models.PositiveSmallIntegerField(default=1, validators=[
        validators.MinValueValidator(
            1, message='Minimum team members must be more than 0.')
    ])
    max_team_members = models.PositiveSmallIntegerField(default=1)
    is_registration_open = models.BooleanField(default=True)

    @property
    def event_day_num(self):
        truncated_schedule = self.schedule.replace(
            hour=0, minute=0, second=0, microsecond=0)
        return settings.EVENT_DAY_NUMS[truncated_schedule]

    def __str__(self):
        return self.event_name


class Team(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    upi_reference_number = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            validators.RegexValidator(
                regex=r'^\d{12}$',
                message='Invalid UPI reference number.'
            )
        ],
        error_messages={
            'max_length': 'Invalid UPI reference number.',
            'unique': 'Invalid UPI reference number.'
        }
    )

    def __str__(self):
        return str(self.id)


class Member(models.Model):
    team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.CASCADE)
    member_name = custom_fields.LowerCharField(max_length=50)
    email = custom_fields.LowerEmailField()
    mobile = models.CharField(
        max_length=10,
        validators=[
            validators.RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Moblie number must be a valid Indian moblie number.'
            )
        ],
        error_messages={
            'max_length': 'Mobile number can have 10 digits at most.'
        }
    )
    university_name = models.CharField(max_length=60)
    course_name = models.CharField(max_length=60)
    residence_area = models.CharField(max_length=60)
    is_registrant = models.BooleanField()

    def save(self, *args, **kwargs):
        if self.team is None:
            # make sure to handle ValidationError on save
            raise ValidationError({'team': 'Team cannot be null.'})

        super().save(*args, **kwargs)

    def __str__(self):
        return self.member_name
