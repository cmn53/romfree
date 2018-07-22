# Generated by Django 2.0.7 on 2018-07-22 02:20

import json
from django.db import migrations
from django.contrib.gis.db import models


def load_image_data(apps, schema_editor):
    Hotel = apps.get_model('rom', 'Hotel')
    Image = apps.get_model('rom', 'Image')

    with open('rom/fixtures/image_data.json') as json_file:
        data = json.load(json_file)

        for d in data:
            try:
                hotel = Hotel.objects.get(hotel_code = d["hotel_code"])
                image = Image(
                    hotel = hotel,
                    image_type = d["image_type"],
                    path = d["path"],
                    order = d["order"]
                )
                image.save()
            except:
                print("Could not add image for hotel %s" %d["hotel_code"])
                pass

class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0005_image'),
    ]

    operations = [
        migrations.RunPython(load_image_data)
    ]
