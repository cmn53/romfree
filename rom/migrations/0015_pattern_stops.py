# Generated by Django 2.0.7 on 2018-07-22 02:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0014_auto_20180722_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='pattern',
            name='stops',
            field=models.ManyToManyField(to='rom.Stop'),
        ),
    ]