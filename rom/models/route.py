from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiLineString
from .operator import Operator

class Route(models.Model):
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)
    route_onestop_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50, blank=True, null=True)
    long_name = models.CharField(max_length=100, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=6, blank=True, null=True)
    geom = models.MultiLineStringField(spatial_index=True)

    def __str__(self):
        return "%s Route %s" %(self.operator.name, self.name)
