# Generated by Django 2.0.7 on 2018-07-22 02:42

import json
from django.db import migrations, transaction
from django.contrib.gis.db import models


def load_pattern_data(apps, schema_editor):
    Route = apps.get_model('rom', 'Route')
    Pattern = apps.get_model('rom', 'Pattern')

    with open('rom/fixtures/pattern_data.json') as json_file:
        data = json.load(json_file)

        for d in data:
            try:
                with transaction.atomic():
                    route = Route.objects.get(route_onestop_id = d["route_onestop_id"])
                    pattern = Pattern(
                        route = route,
                        pattern_onestop_id = d["pattern_onestop_id"],
                        wk_trips = d["wk_trips"],
                        sa_trips = d["sa_trips"],
                        su_trips = d["su_trips"],
                        core_trips = d["core_trips"]
                    )
                    pattern.save()
            except Exception as e:
                print("%s" %e)
                pass


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0011_pattern'),
    ]

    operations = [
        migrations.RunPython(load_pattern_data)
    ]
