# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0007_auto_20150730_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='slug',
            field=models.SlugField(editable=False),
        ),
    ]
