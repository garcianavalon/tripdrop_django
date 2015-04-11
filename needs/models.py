from django.db import models
from django_countries.fields import CountryField

class ContactPerson(models.Model):
    name = models.CharField(max_length=50)
    relation_with_institution = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=20)

class Country(models.Model):
    name = CountryField()

class Region(models.Model):
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=20)

class City(models.Model):
    region = models.ForeignKey(Country)
    name = models.CharField(max_length=20)

class Need(models.Model):
    NEED_TYPES = (
        ('MA', 'Material'),
        ('SE', 'Sevicios(talleres/voluntariado)'),
    )
    need_type = models.CharField(
        max_length=2, choices=NEED_TYPES)
    petition = models.CharField(max_length=500)
    places_to_visit = models.CharField(max_length=300)
    pub_date = models.DateTimeField('date published')
    mod_date = models.DateTimeField('date last modified')
    city = models.ForeignKey(max_length=20)
    contact_persons = models.ManyToManyField(ContactPerson)
    # TODO(garcianavalon) geo localization
    # TODO(garcianavalon) 0+ images
    # TODO(garcianavalon) 0+ youtube videos

class Institution(models.Model):
    INSTITUTION_TYPES = (
        ('ED', 'Educativo'),
        ('SA', 'Sanitario'),
        ('SO', 'Social'),
        ('ON', 'ONG'),
        ('RE', 'Religioso'),
        ('OT', 'Otros'),
    )
    institution_type = models.CharField(
        max_length=2, choices=INSTITUTION_TYPES)
    name = models.CharField(max_length=20)
    needs = models.ManyToManyField(Need)
    description = models.CharField(max_length=300)

        