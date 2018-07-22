from django.contrib.gis.db import models
from django.db.models import Max
from math import log10
from .hotel import Hotel
from .arrival import Arrival


class Score(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, primary_key=True)
    qtr_trips = models.IntegerField()
    qtr_freq_trips = models.IntegerField()
    qtr_dest = models.IntegerField()
    qtr_dest_trips = models.IntegerField()
    half_trips = models.IntegerField()
    half_freq_trips = models.IntegerField()
    half_dest = models.IntegerField()
    half_dest_trips = models.IntegerField()

    def __str__(self):
        return ("Score: hotel %d" %self.hotel.id)
