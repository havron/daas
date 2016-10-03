# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daasapp', '0002_drone_owner_id_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='drone',
            name='owner_id_num',
        ),
    ]
