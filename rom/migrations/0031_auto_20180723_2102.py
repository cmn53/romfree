# Generated by Django 2.0.7 on 2018-07-23 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0030_auto_20180723_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelDestination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distance', models.FloatField()),
                ('mode', models.CharField(max_length=50)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rom.Destination')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rom.Hotel')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='destinations',
            field=models.ManyToManyField(through='rom.HotelDestination', to='rom.Destination'),
        ),
    ]