from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from .metro import Metro
from .stop import Stop
from .pattern import Pattern

class Arrival(models.Model):
    metro = models.ForeignKey(Metro, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    geom = models.PointField(spatial_index=True)

    def __str__(self):
        return self.name
