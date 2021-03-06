from django.contrib.gis.db import models
from django.contrib.gis.measure import Distance
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
    qtr_static_score = models.FloatField(default=0)
    half_trips = models.IntegerField()
    half_freq_trips = models.IntegerField()
    half_dest = models.IntegerField()
    half_dest_trips = models.IntegerField()
    half_static_score = models.FloatField(default=0)

    def __str__(self):
        return ("Score: hotel %d" %self.hotel.id)

    # def qtr_static_score(self):
    #     if self.qtr_trips == 0:
    #         return 0
    #     else:
    #         max = Score.objects.aggregate(Max('qtr_trips'), Max('qtr_freq_trips'), Max('qtr_dest_trips'))
    #         trips = log10(self.qtr_trips)
    #         freq_trips = log10(self.qtr_freq_trips) if self.qtr_freq_trips else 0
    #         dest_trips = log10(self.qtr_dest_trips) if self.qtr_dest_trips else 0
    #         static_score = trips * 30/log10(max['qtr_trips__max']) + freq_trips * 30/log10(max['qtr_freq_trips__max']) + dest_trips * 30/log10(max['qtr_dest_trips__max'])
    #         return static_score
    #
    # def half_static_score(self):
    #     if self.half_trips == 0:
    #         return 0
    #     else:
    #         max = Score.objects.aggregate(Max('half_trips'), Max('half_freq_trips'), Max('half_dest_trips'))
    #         trips = log10(self.half_trips)
    #         freq_trips = log10(self.half_freq_trips) if self.half_freq_trips else 0
    #         dest_trips = log10(self.half_dest_trips) if self.half_dest_trips else 0
    #         static_score = trips * 30/log10(max['half_trips__max']) + freq_trips * 30/log10(max['half_freq_trips__max']) + dest_trips * 30/log10(max['half_dest_trips__max'])
    #         return static_score


    # def arrival_score(self, radius, arrival_id):
    #     arrival_patterns = Arrival.objects.get(id=arrival_id).nearby_patterns(radius)
    #     hotel_patterns = self.hotel.nearby_patterns(radius)
    #     if arrival_patterns.filter(pk__in=hotel_patterns):
    #         if distance
    #     else:
    #         return 0
