# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0004_auto_20150730_1342'),
    ]

    operations = [
        migrations.AddField(
            model_name='need',
            name='country',
            field=models.ForeignKey(default=1, to='needs.Country'),
            preserve_default=False,
        ),
    ]
