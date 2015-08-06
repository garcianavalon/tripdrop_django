# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='institution',
            name='needs',
        ),
        migrations.AddField(
            model_name='need',
            name='institution_description',
            field=models.CharField(default='desc', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='need',
            name='institution_type',
            field=models.CharField(default='ED', max_length=2, choices=[(b'ED', b'Educativo'), (b'SA', b'Sanitario'), (b'SO', b'Social'), (b'ON', b'ONG'), (b'RE', b'Religioso'), (b'OT', b'Otros')]),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Institution',
        ),
    ]
