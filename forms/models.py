from django.db import models
from django.utils.translation import gettext_lazy as _
from tech_kaushalya.custom_fields import custom_fields

# Create your models here.


class Updates(models.Model):
    email = custom_fields.LowerEmailField(
        _('email'),
        unique=True,
        error_messages={
            'unique': _('Email already registered.'),
        },
    )
