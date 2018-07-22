# Generated by Django 2.0.7 on 2018-07-22 02:46

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0012_auto_20180722_0242'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stop_onestop_id', models.CharField(max_length=100)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
