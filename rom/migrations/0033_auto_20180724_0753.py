# Generated by Django 2.0.7 on 2018-07-24 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0032_auto_20180723_2102'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['-pattern__core_trips']},
        ),
        migrations.AddField(
            model_name='hoteldestination',
            name='routes',
            field=models.ManyToManyField(to='rom.Route'),
        ),
    ]
