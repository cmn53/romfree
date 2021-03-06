# Generated by Django 2.0.7 on 2018-07-22 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rom', '0006_auto_20180722_0220'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=50)),
                ('operator_onestop_id', models.CharField(max_length=100)),
                ('metro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rom.Metro')),
            ],
        ),
    ]
