# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='need',
            name='city',
            field=models.CharField(default='madrid', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='location',
            field=location_field.models.plain.PlainLocationField(default='test', max_length=63),
            preserve_default=False,
        ),
    ]
