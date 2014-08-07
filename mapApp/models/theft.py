from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


THEFT_CHOICES = (
    ('Bike', 'Bike'),
    ('Major bike component', 'Major bike component (e.g. tire, seat, handlebars, etc.)'),
    ('Minor bike component', 'Minor bike component (e.g. lights, topbar padding, bell, etc.)')
)
BOOLEAN_CHOICES = (
    ('Y', 'Yes'), 
    ('N', 'No'), 
    ('I don\'t know', 'I don\'t know')
)
HOW_LOCKED_CHOICES = (
    ('Frame locked', 'Frame locked'),
    ('Frame and tire locked', 'Frame and tire locked'),
    ('Frame and both tires locked', 'Frame and both tires locked'),
    ('Tire(s) locked', 'Tire(s) locked'),
    ('Not locked', 'Not locked')
)
LOCK_CHOICES = (
    ('U-Lock', 'U-Lock'),
    ('Cable lock', 'Cable lock'),
    ('U-Lock and cable', 'U-Lock and cable'),
    ('Padlock', 'Padlock'),
    ('Not locked', 'Not locked')
)
LOCKED_TO_CHOICES = (
    ('Outdoor bike rack', 'Outdoor bike rack'),
    ('Indoor bike rack', 'Indoor bike rack (e.g. parking garage, bike room)'),
    ('Bike locker', 'Bike locker'),
    ('Street sign', 'Street sign'),
    ('Fence', 'Fence'),
    ('Bench', 'Bench'),
    ('Railing', 'Railing'),
    ('Other', 'Other'),
    ('Not locked', 'Not locked')
)

##########
# Theft class.
# Class for Theft Reports. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
class Theft(models.Model):
    ########### THEFT FIELDS
    date = models.DateTimeField(
        'Date reported', 
        auto_now_add=True   # Date is set automatically when object created
    ) 
    # Spatial fields
    # Default CRS -> WGS84
    geom = models.PointField(
        'Location'
    )
    objects = models.GeoManager() # Required to conduct geographic queries

    theft_date = models.DateTimeField(
        'When did notice that you had been robbed?'
    )

    theft = models.CharField(
        'What was stolen?', 
        max_length=100, 
        choices=THEFT_CHOICES
    )

    was_locked = models.BooleanField(
        'Was your bike locked?',
        choices=((True, 'Yes'),(False, 'No'))
    )
    
    how_locked = models.CharField(
        'How did you have your bike locked?',
        max_length=100,
        choices=HOW_LOCKED_CHOICES
    )

    lock = models.CharField(
        'What kind of lock were you using?',
        max_length=100,
        choices=LOCK_CHOICES
    )

    locked_to = models.CharField(
        'What was your bike locked to?',
        max_length=100,
        choices=LOCKED_TO_CHOICES
    )

    police_report = models.NullBooleanField(
        'Did you file a report with the police?',
        choices=((True, 'Yes'),(False, 'No'))
    )

    insurance_claim = models.NullBooleanField(
        'Did you file an insurance claim?',
        choices=((True, 'Yes'),(False, 'No'))
    )
    ###########

    regular_cyclist = models.CharField(
        'Do you ride a bike often? (52+ times/year)',
        max_length=20, 
        choices=BOOLEAN_CHOICES, 
        blank=True, 
        null=True
    )
    #######################

    ########## DETAILS FIELDS
    theft_detail = models.TextField(
        'Please give a brief description about what happened.', 
        max_length=300, 
        blank=True, 
        null=True
    )
    ##############

    # reverses latlngs and turns tuple of tuples into list of lists
    def latlngList(self):
        return list(self.geom)[::-1]   

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(weeks=1) <= self.date < now

    def incident_type(self):
        return "Theft"

    # For admin site 
    was_published_recently.admin_order_field = 'date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.theft_date)

    class Meta:
        app_label = 'mapApp'