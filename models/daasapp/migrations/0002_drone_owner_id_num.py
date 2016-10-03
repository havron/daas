# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daasapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='drone',
            name='owner_id_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
