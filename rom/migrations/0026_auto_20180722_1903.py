# Generated by Django 2.0.7 on 2018-07-22 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0025_auto_20180722_1846'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotelarrival',
            name='arrival_score',
        ),
        migrations.AddField(
            model_name='hotelarrival',
            name='half_arrival_score',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='hotelarrival',
            name='qtr_arrival_score',
            field=models.FloatField(default=0),
        ),
    ]
