# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0002_auto_20150806_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstitutionTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='need',
            name='institution_type',
        ),
        migrations.AddField(
            model_name='need',
            name='institution_type',
            field=models.ManyToManyField(to='needs.InstitutionTypes'),
        ),
    ]
