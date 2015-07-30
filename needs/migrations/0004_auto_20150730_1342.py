# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('needs', '0003_auto_20150411_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('country', models.ForeignKey(to='needs.Country')),
            ],
        ),
        migrations.RemoveField(
            model_name='city',
            name='region',
        ),
        migrations.RemoveField(
            model_name='region',
            name='country',
        ),
        migrations.RemoveField(
            model_name='need',
            name='city',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.AddField(
            model_name='need',
            name='municipality',
            field=models.ForeignKey(default=1, to='needs.Municipality'),
            preserve_default=False,
        ),
    ]
