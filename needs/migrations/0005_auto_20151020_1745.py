# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0004_auto_20151020_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='need',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='need',
            name='lon',
        ),
        migrations.AddField(
            model_name='need',
            name='geolocation_results',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
