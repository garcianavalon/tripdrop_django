# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='mod_date',
            field=models.DateTimeField(auto_now=True, verbose_name=b'date last modified'),
        ),
        migrations.AlterField(
            model_name='need',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'date published'),
        ),
    ]
