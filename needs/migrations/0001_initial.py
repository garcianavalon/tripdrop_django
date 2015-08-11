# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('relation_with_institution', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Need',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institution_description', models.CharField(max_length=300)),
                ('title', models.CharField(max_length=40)),
                ('need_type', models.CharField(max_length=2, choices=[(b'MA', b'Material'), (b'SE', b'Sevicios(talleres/voluntariado)')])),
                ('petition', models.CharField(max_length=500)),
                ('places_to_visit', models.CharField(max_length=300)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name=b'date published')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name=b'date last modified')),
                ('slug', models.SlugField(editable=False)),
                ('contact_persons', models.ManyToManyField(to='needs.ContactPerson', blank=True)),
                ('institution_type', models.ManyToManyField(to='needs.InstitutionType')),
                ('municipality', models.ForeignKey(to='needs.Municipality')),
            ],
        ),
    ]
