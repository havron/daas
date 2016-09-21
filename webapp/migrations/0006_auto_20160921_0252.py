# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_drone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='last_checked_out',
            field=models.TextField(),
        ),
    ]
