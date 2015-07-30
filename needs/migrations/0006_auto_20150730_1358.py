# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0005_need_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='need',
            name='contact_persons',
            field=models.ManyToManyField(to='needs.ContactPerson', blank=True),
        ),
        migrations.AlterField(
            model_name='need',
            name='country',
            field=models.ForeignKey(to='needs.Country', blank=True),
        ),
        migrations.AlterField(
            model_name='need',
            name='municipality',
            field=models.ForeignKey(to='needs.Municipality', blank=True),
        ),
    ]
