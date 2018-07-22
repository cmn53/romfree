from django.contrib.gis.db import models
from .route import Route
from .stop import Stop

class Pattern(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    pattern_onestop_id = models.CharField(max_length=100)
    wk_trips = models.IntegerField(default=0)
    sa_trips = models.IntegerField(default=0)
    su_trips = models.IntegerField(default=0)
    core_trips = models.IntegerField(default=0)
    stops = models.ManyToManyField(Stop)

    def __str__(self):
        return "%s Pattern %s" %(self.route.operator.name, self.pattern_onestop_id)
