# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0002_auto_20150411_1711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='need',
            old_name='pub_date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='need',
            old_name='mod_date',
            new_name='modified_at',
        ),
    ]
