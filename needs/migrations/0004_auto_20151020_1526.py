# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0003_auto_20151020_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='need',
            name='lat',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='lon',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='postal_address',
            field=models.CharField(max_length=300, blank=True),
        ),
    ]
