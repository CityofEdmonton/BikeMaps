from django.utils.translation import ugettext as _
from django.conf import settings

from django.contrib.gis.db import models

import datetime
from django.utils import timezone


############
# Response options for CharField data types
# 
INCIDENT_CHOICES = (
    ('Collision', (
            ('Single vehicle striking fixed object','Single vehicle striking fixed object (e.g., curb, sign, planter)'),
            ('Single vehicle striking a moving object', 'Single vehicle striking a moving object (e.g., pedestrian, inline skater, animal)'),
            ('Multi vehicle collision with moving vehicle', 'Multi vehicle collision with moving vehicle'),
            ('Multi vehicle collision with parked vehicle', 'Multi vehicle collision with parked vehicle'),
        )
    ),
    ('Near miss', (
            ('Near collision with a fixed object', 'Near collision with a fixed object (e.g., curb, sign, planter)'),
            ('Near collision with a moving object', 'Near collision with a moving object (e.g., pedestrian, inline skater, animal)'),
            ('Near collision with a moving vehicle', 'Near collision with a moving vehicle'),
            ('Near collision with a parked vehicle', 'Near collision with a parked vehicle'),
        )
    ),
    ('Fall', (
            ('Single vehicle losing control', 'Single vehicle losing control'),
        )
    )
)
INCIDENT_WITH_CHOICES = [
    ('Car/Truck', 'Car/Truck'),
    ('Vehicle door', 'Vehicle door'),
    ('Another cyclist', 'Another cyclist'),
    ('Curb', 'Curb'),
    ('Pedestrian/Person', 'Pedestrian/Person'),
    ('Train Tracks', 'Train Tracks'),
    ('Pothole', 'Pothole'),
    ('Lane divider', 'Lane divider'),
    ('Animal', 'Animal'),
    ('Sign/Post', 'Sign/Post'),
    ('Roadway', 'Roadway')
]

INJURY_CHOICES = [
    ('No injury', 'No injury'),
    ('Injury, no treatment', 'Injury, no medical treatment'),
    ('Injury, saw family doctor', 'Injury, saw family doctor'),
    ('Injury, hospital emergency visit', 'Injury, visited hospital emergency dept.'),
    ('Injury, hospitalized', 'Injury, hospitalized (i.e. stayed overnight in hospital dept. other than emergency)')
]

PURPOSE_CHOICES = (
    ("Commute", "To/from work or school"), 
    ("Exercise or recreation", "Exercise or recreation"), 
    ("Social reason", "Social reason (e.g., movies, visit friends)"), 
    ("Personal business", "Personal business"),
    ("During work", "During work")
)
ROAD_COND_CHOICES = (
    ('Dry', 'Dry'),
    ('Wet','Wet'),
    ('Loose sand, gravel, or dirt', 'Loose sand, gravel, or dirt'),
    ('Icy','Icy'),
    ('Snowy','Snowy'),
    ('Don\'t remember', 'I don\'t remember')
)
SIGHTLINES_CHOICES = (
    ('No', 'No'),
    ('View obstructed', 'View obstructed'),
    ('Glare or reflection', 'Glare or reflection'),
    ('Obstruction on road', 'Obstruction on road'),
    ('Don\'t Remember', 'Don\'t Remember')
)
RIDING_ON_CHOICES = (
    ('Busy street', (
            ('Busy street bike lane', 'On a painted bike lane'),
            ('Busy street, no bike facilities', 'On road with no bike facilities')
        )
    ),
    ('Quiet street', (
            ('Quiet street bike lane', 'On a painted bike lane'),
            ('Quiet street, no bike facilities', 'On road with no bike facilities')
        )
    ),
    ('Not on the street', (
            ('Cycle track', 'On a physically separated bike lane (cycle track)'),
            ('Mixed use trail', 'On a mixed use trail'),
            ('Sidewalk', 'On the sidewalk'),
        )
    ),
    ('Don\'t remember', 'I don\'t remember')
)
LIGHTS_CHOICES = (
    ("NL", "No Lights"),
    ("FB", "Front and back lights"),
    ("F", "Front lights only"),
    ("B", "Back lights only"),
    ('Don\'t remember', 'I don\'t remember')

)
TERRAIN_CHOICES = (
    ('Uphill', 'Uphill'), 
    ('Downhill','Downhill'),
    ('Flat', 'Flat'),
    ('Don\'t remember', 'I don\'t remember')
)
AGE_CHOICES = (
    ("<19", "19 or under"),
    ("19-29","19 - 29"),
    ("30-39", "30 - 39"),
    ("40-49", "40 - 49"),
    ("50-59","50 - 59"),
    ("60-69","60 - 69"),
    (">70", "70 or over")
)
SEX_CHOICES = (
    ('M', 'Male'), 
    ('F', 'Female'),
    ('Other', 'Other')
)
BOOLEAN_CHOICES = (
    ('Y', 'Yes'), 
    ('N', 'No'), 
    ('I don\'t know', 'I don\'t know')
)


##########
# Incident class.
# Main class for Incident Report. Contains all required, non-required, and spatial fields. Setup to allow easy export to a singular shapefile.
# Captures all data about the accident and environmental conditions when the bike incident occurred.
class Incident(models.Model):
    ########### INCIDENT FIELDS
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

    incident_date = models.DateTimeField(
        'When was the incident?'
    )

    incident = models.CharField(
        'What type of incident was it?', 
        max_length=150, 
        choices=INCIDENT_CHOICES
    )

    incident_with = models.CharField(
        'What sort of object was the collision or near collision with?',
        max_length=100,
        choices=INCIDENT_WITH_CHOICES
    )

    # Injury details (all optional)
    injury = models.CharField(
        'Were you injured?',
        max_length=30,
        choices= INJURY_CHOICES # Without this, field has 'Unknown' for None rather than the desired "---------"
    )

    trip_purpose = models.CharField(
        'What was the purpose of your trip?', 
        max_length=50, 
        choices=PURPOSE_CHOICES, 
        blank=True, 
        null=True
    )
    ###########

    ############## PERSONAL DETAILS FIELDS
    # Personal details about the participant (all optional)
    age = models.CharField(
        'Please tell us which age category you fit into', 
        max_length=15, 
        choices=AGE_CHOICES, 
        blank=True, 
        null=True
    ) 
    sex = models.CharField(
        'Please select your sex', 
        max_length=10, 
        choices=SEX_CHOICES, 
        blank=True, 
        null=True
    )
    regular_cyclist = models.CharField(
        'Do you bike at least once a week?',
        max_length=30, 
        choices=BOOLEAN_CHOICES, 
        blank=True, 
        null=True
    )
    helmet = models.CharField(
        'Were you wearing a helmet?',
        max_length=30, 
        choices=BOOLEAN_CHOICES, 
        blank=True, 
        null=True
    )
    intoxicated = models.CharField(
    'Were you intoxicated?',
    max_length=30, 
    choices=BOOLEAN_CHOICES, 
    blank=True, 
    null=True
    )
    #######################

    ############### CONDITIONS FIELDS
    road_conditions = models.CharField(
        'What were the road conditions?', 
        max_length=30, 
        choices=ROAD_COND_CHOICES, 
        blank=True, 
        null=True
    )
    sightlines = models.CharField(
        'How were the sight lines?', 
        max_length=30, 
        choices=SIGHTLINES_CHOICES, 
        blank=True, 
        null=True
    )
    cars_on_roadside = models.CharField(
        'Were there cars parked on the roadside',
        max_length=30, 
        choices= BOOLEAN_CHOICES,
        blank=True, 
        null=True
    )
    riding_on = models.CharField(
        'Where were you riding your bike?', 
        max_length=30, 
        choices=RIDING_ON_CHOICES, 
        blank=True, 
        null=True
    )
    bike_lights = models.CharField(
        'Were you using bike lights?', 
        max_length=200, 
        choices=LIGHTS_CHOICES, 
        blank=True, 
        null=True
    )
    terrain = models.CharField(
        'What was the terrain like?', 
        max_length=30, 
        choices=TERRAIN_CHOICES, 
        blank=True, 
        null=True
    )
    ########################

    ########## DETAILS FIELDS
    incident_detail = models.TextField(
        'Please give a brief description of the incident', 
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
        for (kind, choices) in INCIDENT_CHOICES:
            for c in choices:
                if self.incident in c: return kind

    # For admin site 
    was_published_recently.admin_order_field = 'date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Reported this week?'

    # toString()
    def __unicode__(self):
        return unicode(self.incident_date)

    class Meta:
        app_label = 'mapApp'