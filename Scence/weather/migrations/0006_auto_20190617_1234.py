# Generated by Django 2.2.1 on 2019-06-17 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0005_auto_20190617_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='href',
            field=models.CharField(max_length=128, verbose_name='城市历史数据入口'),
        ),
    ]