# Generated by Django 2.0.7 on 2018-07-22 03:29

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0018_auto_20180722_0326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('metro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rom.Metro')),
            ],
        ),
    ]
