# Generated by Django 2.2.1 on 2019-06-01 03:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficView', '0008_auto_20190531_1406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citytraffic',
            options={'ordering': ['detailtime']},
        ),
        migrations.RenameField(
            model_name='citytraffic',
            old_name='detailTime',
            new_name='detailtime',
        ),
        migrations.RenameField(
            model_name='citytraffic',
            old_name='TrafficIndex',
            new_name='trafficindex',
        ),
    ]
