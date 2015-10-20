# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0002_auto_20151020_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='city',
        ),
        migrations.RemoveField(
            model_name='need',
            name='location',
        ),
    ]
