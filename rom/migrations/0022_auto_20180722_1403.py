# Generated by Django 2.0.7 on 2018-07-22 14:03

import json
from django.db import migrations
from django.contrib.gis.db import models

def load_score_data(apps, schema_editor):
    Score = apps.get_model('rom', 'Score')
    Hotel = apps.get_model('rom', 'Hotel')

    with open('rom/fixtures/score_data.json') as json_file:
        data = json.load(json_file)

        for d in data:
            try:
                hotel = Hotel.objects.get(id = d["hotel_id"])
                score = Score(
                    hotel = hotel,
                    qtr_trips = d["qtr_trips"],
                    qtr_freq_trips = d["qtr_freq_trips"],
                    qtr_dest = d["qtr_dest"],
                    qtr_dest_trips = d["qtr_dest_trips"],
                    half_trips = d["half_trips"],
                    half_freq_trips = d["half_freq_trips"],
                    half_dest = d["half_dest"],
                    half_dest_trips = d["half_dest_trips"]
                )
                score.save()
            except Exception as e:
                print("%s" %e)
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0021_score'),
    ]

    operations = [
        migrations.RunPython(load_score_data)
    ]