# Generated by Django 2.2.1 on 2019-05-30 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TrafficView', '0005_auto_20190530_1335'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadtraffic',
            name='flag',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]