# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('model_name', models.CharField(max_length=50)),
                ('drone_desc', models.TextField()),
                ('demo_link', models.URLField()),
                ('permissions', models.CharField(max_length=50)),
                ('owner_email', models.EmailField(max_length=254)),
                ('battery_level', models.FloatField()),
                ('maintenance_status', models.TextField()),
                ('available_for_hire', models.BooleanField()),
                ('last_checked_out', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('username', models.CharField(unique=True, max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254)),
                ('date_joined', models.DateTimeField()),
                ('is_active', models.BooleanField()),
                ('f_name', models.CharField(max_length=16)),
                ('l_name', models.CharField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='drone',
            name='owner',
            field=models.ForeignKey(to='daasapp.User'),
        ),
    ]
