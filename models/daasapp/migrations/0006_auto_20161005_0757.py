# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daasapp', '0005_auto_20161005_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drone',
            name='permissions',
            field=models.TextField(),
        ),
    ]
