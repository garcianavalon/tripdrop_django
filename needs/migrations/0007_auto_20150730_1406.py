# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0006_auto_20150730_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='need',
            name='slug',
            field=models.SlugField(default='slug'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='title',
            field=models.CharField(default='title', max_length=40),
            preserve_default=False,
        ),
    ]
