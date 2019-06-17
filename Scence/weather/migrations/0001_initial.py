# Generated by Django 2.2.1 on 2019-06-17 02:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='城市名')),
                ('citypid', models.IntegerField(unique=True, verbose_name='城市唯一标识')),
            ],
            options={
                'db_table': 'city',
            },
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='省份')),
                ('provincepid', models.IntegerField(unique=True, verbose_name='省份唯一标识')),
            ],
            options={
                'db_table': 'province',
            },
        ),
        migrations.CreateModel(
            name='WeatherManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('historypid', models.IntegerField(unique=True, verbose_name='历史天气id')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='WeatherManager', to='weather.City', to_field='citypid')),
            ],
            options={
                'db_table': 'weathermanager',
            },
        ),
        migrations.CreateModel(
            name='HistoryWeather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('state', models.TextField(verbose_name='天气状况')),
                ('temperature', models.TextField(verbose_name='气温')),
                ('wind', models.TextField(verbose_name='风力风向')),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='History', to='weather.WeatherManager', to_field='historypid')),
            ],
            options={
                'db_table': 'history',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Pid', to='weather.Province', to_field='provincepid'),
        ),
    ]