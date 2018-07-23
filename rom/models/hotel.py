from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.contrib.gis.db.models import Collect
from django.db.models import Sum
from .metro import Metro
from .stop import Stop
from .pattern import Pattern
from .route import Route
from .arrival import Arrival
from .destination import Destination
import json

class HotelArrival(models.Model):
    hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
    arrival = models.ForeignKey(Arrival, on_delete=models.CASCADE)
    distance = models.FloatField()
    qtr_arrival_score = models.FloatField(default=0)
    half_arrival_score = models.FloatField(default=0)

    class Meta:
        ordering = ['-hotel__score__qtr_static_score', '-qtr_arrival_score']

    @property
    def total_qtr_score(self):
        return int(self.hotel.score.qtr_static_score + self.qtr_arrival_score)

    @property
    def total_half_score(self):
        return int(self.hotel.score.half_static_score + self.half_arrival_score)

    @classmethod
    def load_qtr_arrival_scores(cls):
        for ha in HotelArrival.objects.all():
            arrival_patterns = ha.arrival.nearby_patterns(0.25)
            hotel_patterns = ha.hotel.nearby_patterns(0.25)

        if arrival_patterns.filter(pk__in=hotel_patterns):
            if ha.distance < 10:
                ha.qtr_arrival_score = 10
            else:
                ha.qtr_arrival_score = 5
        else:
            ha.qtr_arrival_score = 0
        ha.save()

    @classmethod
    def load_half_arrival_scores(cls):
        for ha in HotelArrival.objects.all():
            arrival_patterns = ha.arrival.nearby_patterns(0.5)
            hotel_patterns = ha.hotel.nearby_patterns(0.5)

        if arrival_patterns.filter(pk__in=hotel_patterns):
            if ha.distance < 10:
                ha.half_arrival_score = 10
            else:
                ha.half_arrival_score = 5
        else:
            ha.half_arrival_score = 0
        ha.save()




class Hotel(models.Model):
    hotel_code = models.IntegerField()
    name = models.CharField(max_length=200)
    metro = models.ForeignKey(Metro, on_delete=models.CASCADE)
    geom = models.PointField(spatial_index=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    arrivals = models.ManyToManyField(Arrival, through=HotelArrival, through_fields=('hotel', 'arrival'),)

    def __str__(self):
        return self.name

    def nearby_stops(self, radius):
        stops = Stop.objects.filter(geom__distance_lte=(self.geom, Distance(mi=radius)))
        return stops

    def nearby_patterns(self, radius):
        stops = self.nearby_stops(radius)
        patterns = Pattern.objects.filter(stops__in=stops).distinct()
        return patterns

    # may not even need this one for the score?
    # def nearby_routes(self):
    #     patterns = self.nearby_patterns()
    #     routes = Route.objects.filter(pattern__in=patterns).distinct()
    #     return routes

    def get_weekly_trips(self, radius):
        patterns = self.nearby_patterns(radius)
        total_weekly_trips = 0
        for p in patterns:
            total_weekly_trips += p.weekly_trips
        return total_weekly_trips


    def get_frequent_trips(self, radius):
        patterns = self.nearby_patterns(radius)
        trips_by_route = Route.objects.values('long_name') \
            .filter(pattern__in=patterns) \
            .annotate(
                core_trips=Sum('pattern__core_trips')
            )

        frequent_trips = 0
        # 96 trips over a 12 hour period (6am-6pm) represents an average headway of 15 minutes for bidirectional service
        # 18 trips over a 3 hour period (6pm-9pm) represents an average headway of 20 minutes for bidirectional service
        for r in trips_by_route:
            if r["core_trips"] > 114:
                frequent_trips += r["core_trips"]

        return frequent_trips


    # Using this method in place of get_destinations_served is much faster provides less robust information
    # def get_trips_serving_destinations(self, radius):
    #     destination_set = Destination.objects.filter(metro=self.metro).aggregate(Collect("geom"))
    #     destination_stops = Stop.objects.filter(geom__distance_lte=(destination_set["geom__collect"], Distance(mi=radius)))
    #     destination_patterns = Pattern.objects.filter(stops__in=destination_stops).distinct()
    #
    #     hotel_patterns = self.nearby_patterns(radius)
    #
    #     intersect_patterns = hotel_patterns.filter(pk__in=destination_patterns)
    #
    #     total_weekly_trips = 0
    #     for p in intersect_patterns:
    #         total_weekly_trips += p.weekly_trips
    #
    #     return total_weekly_trips


    def get_destinations_served(self, radius):
        destinations_served = {}
        hotel_patterns = self.nearby_patterns(radius)
        destinations = Destination.objects.filter(metro=self.metro)
        for d in destinations:
            destination_patterns = d.nearby_patterns(radius)
            intersect_patterns = hotel_patterns.filter(pk__in=destination_patterns)
            if intersect_patterns:
                total_weekly_trips = 0
                for p in intersect_patterns:
                    total_weekly_trips += p.weekly_trips
                destinations_served[d.name] = total_weekly_trips
        return destinations_served


    @classmethod
    def write_score_elements(cls):
        hotel_scores = []
        for h in Hotel.objects.all():
            qtr_dest = h.get_destinations_served(0.25)
            half_dest = h.get_destinations_served(0.5)
            hotel_scores.append(
                {
                    "hotel_id": h.id,
                    "qtr_trips": h.get_weekly_trips(0.25),
                    "qtr_freq_trips": h.get_frequent_trips(0.25),
                    "qtr_dest": len(qtr_dest),
                    "qtr_dest_trips": sum(qtr_dest.values()),
                    "half_trips": h.get_weekly_trips(0.5),
                    "half_freq_trips": h.get_frequent_trips(0.5),
                    "half_dest": len(half_dest),
                    "half_dest_trips": sum(half_dest.values())
                }
            )
            print("Finished number crunching for hotel %s" %h.id)

        with open('rom/fixtures/score_data.json', 'w') as f:
            json.dump(hotel_scores, f)

        return "Successfully wrote scoring data to file"
