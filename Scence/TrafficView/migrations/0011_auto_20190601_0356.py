# Generated by Django 2.2.1 on 2019-06-01 03:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficView', '0010_auto_20190601_0350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='yearcitytraffic',
            old_name='TrafficIndex',
            new_name='trafficindex',
        ),
    ]