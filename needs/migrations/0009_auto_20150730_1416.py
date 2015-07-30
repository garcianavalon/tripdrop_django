# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0008_auto_20150730_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='country',
            field=models.ForeignKey(to='needs.Country'),
        ),
        migrations.AlterField(
            model_name='need',
            name='municipality',
            field=models.ForeignKey(to='needs.Municipality'),
        ),
    ]
