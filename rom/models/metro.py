from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


class Metro(models.Model):
    name = models.CharField(max_length=50)
    metro_code = models.CharField(max_length=3)
    country_code = models.CharField(max_length=2)
    centroid = models.PointField(spatial_index=True)
    nw_bound = models.PointField(spatial_index=True)
    se_bound = models.PointField(spatial_index=True)

    def __str__(self):
        return self.name
