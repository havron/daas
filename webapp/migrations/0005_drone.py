# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('model_name', models.CharField(max_length=50)),
                ('drone_desc', models.TextField()),
                ('demo_link', models.URLField()),
                ('permissions', models.CharField(max_length=50)),
                ('owner_email', models.EmailField(max_length=254)),
                ('last_checked_out', models.DateTimeField()),
                ('battery_level', models.FloatField()),
                ('maintenance_status', models.TextField()),
                ('available_for_hire', models.BooleanField()),
            ],
        ),
    ]
