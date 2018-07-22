from django.contrib.gis.db import models
from django.contrib.gis.geos import Point

class Stop(models.Model):
    stop_onestop_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    geom = models.PointField(spatial_index=True)

    def __str__(self):
        return self.name
