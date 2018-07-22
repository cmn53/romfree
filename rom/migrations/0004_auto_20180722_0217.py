# Generated by Django 2.0.7 on 2018-07-22 02:17

import json
from django.db import migrations
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, GEOSGeometry
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def load_hotel_data(apps, schema_editor):
    Hotel = apps.get_model('rom', 'Hotel')
    Metro = apps.get_model('rom', 'Metro')

    with open('rom/fixtures/hotel_data.json') as json_file:
        data = json.load(json_file)

        for d in data:
            try:
                metro = Metro.objects.get(metro_code = d["metro_code"])
                hotel = Hotel(
                    hotel_code = d["hotel_code"],
                    name = d["name"],
                    metro = metro,
                    geom = GEOSGeometry('POINT(%s %s)' %(d["location"]["longitude"],d["location"]["latitude"])),
                    address = d["address"],
                    city = d["city"],
                    postal_code = d["postal_code"],
                    description = d["description"]
                )

                dist_from_center = hotel.geom.distance(hotel.metro.centroid) * 100 /  0.621371

                if dist_from_center > 100:
                    raise ValidationError(_('Hotel is more than 100 miles from metro center'))

                hotel.save()
            except ValidationError as e:
                print("Could not add hotel %s: %s" %(d["hotel_code"], e.message))
                pass
                
class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0003_hotel'),
    ]

    operations = [
        migrations.RunPython(load_hotel_data)
    ]